from dash.dependencies import Input, Output
from dash import Dash
from flask import Flask, render_template
import flask
import dash_html_components as html
from dash_auth.basic_auth import Auth 
import pathlib
from six import iteritems


def change_flask_server(self, flask_app: Flask, new_route: str):
    """Exchange the flask app and the routes

    Parameters
    ----------
    flask_app : Flask
        The new flask app to base the dash app upon
    new_route : str
        The new route for the dash app
    """
    # Make attributes mutable
    self.config._read_only.remove('routes_pathname_prefix')
    self.config._read_only.remove('requests_pathname_prefix')

    # Set new routes
    self.config.routes_pathname_prefix = new_route
    self.config.requests_pathname_prefix = new_route

    # Make them read only again
    self.config._read_only.append('routes_pathname_prefix')
    self.config._read_only.append('requests_pathname_prefix')

    # Reinit with new flask app
    # Set new urls for dash and build flask Blueprint in new flask app
    self.routes = []
    self.init_app(flask_app)
    
    return self
    

# append new method to class Dash
Dash.change_flask_server = change_flask_server    


def dash_route(app:object, url:str):
    """Decorator for building dash route. route gets passed into dash app by using function change_flask_server
    Inside function has to return DashApplication which needs to be modified with new flask server
    Parameters
    ----------
    app : object
        flask application
    url : str
        url for dash app; should start and end with a /
    """

    # Check if url is ended with a /
    if url[-1] != "/":
        url += "/"


    def wrap_f(func):
        def init_app():
            dash_app = func() # get DashApp-Object
            return dash_app.change_flask_server(app, url) # change flask server and init new url
        return init_app()
        
    return wrap_f


def Dashify(app:Flask):
    """Append to flask application method dash_route
    Usage in flask app: 
    @app.dash_route('new_route')
    def dash():
        return DashApp

    Parameters
    ----------
    app : Flask
        Flask application
    """
    app.dash_route = dash_route.__get__(app)

## Security ##
def _protect_views(self):
    """Method of class Auth.
    Needs to be modified to only change views of dash application in flask server. Super class method overwrites all view functions in flask server object, also non-dash ones.
    """
    # Only views that are from dash app and not flask views / routes
    views_dash_app = [view_name for view_name, view_method in self.app.server.view_functions.items() \
        if view_name.startswith(self._index_view_name)]
    
    for view_name, view_method in iteritems(
                self.app.server.view_functions):
            # check for view name: Needs to be in above list
            if view_name in views_dash_app and view_name != self._index_view_name:
                self.app.server.view_functions[view_name] = \
                    self.auth_wrapper(view_method)

# Overview _protect_views method of class Auth
Auth._protect_views = _protect_views
class BasicAuth(Auth):
    def __init__(self, app, secure_method = None, *args, **kwargs):
        Auth.__init__(self, app, _overwrite_index = True)
        if secure_method is not None:
            self.secure_method = secure_method
        else:
            self.secure_method = app.config['SECURE_METHOD']
        self.args = args
        self.kwargs = kwargs

    def set_security_method(self, secure_method):
        self.secure_method = secure_method

    def is_authorized(self):
        header = flask.request.headers.get('Authorization', None)
        if not header:
            return False
        return self.secure_method(self.args, self.kwargs)
    
    def login_request(self):
        return flask.Response(
            'Login Required',
            headers={'WWW-Authenticate': 'Basic realm="User Visible Realm"'},
            status=401)

    def auth_wrapper(self, f):
        def wrap(*args, **kwargs):
            if not self.is_authorized():
                return flask.Response(status=403)

            response = f(*args, **kwargs)
            return response
        return wrap

    def index_auth_wrapper(self, original_index):
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                # return self.login_request()
                try:
                    errorfile_403 =  pathlib.Path(__file__).Parent.absolute() / "error-templates/403.html"
                    return flask.render_template(errorfile_403), 403
                except:
                    return flask.Response(status=403)
        return wrap


def DashifySecure(app, secure_method):
    """[summary]

    Parameters
    ----------
    app : [type]
        [description]
    secure_method : [type]
        [description]
    """
    app.config['SECURE_METHOD'] = secure_method


def dash_secure(secure_method = None, *args, **kwargs):
    """Make dash app secure with own security method. Accepts an method to check for security and further parameters necessary for security method.
    Instantiates BasicAuth object for dash app.
    Important: Decorator Needs to be put above dash routing because Auth modifies view functions of flask server!
    Parameters
    ----------
    secure_method : function
        security method. Can also be set by using DashifySecure function
    """
    def gen_auth(app):
        """Generates the BasicAuth Object

        Parameters
        ----------
        app : Dash
            dash object
        """
        return BasicAuth(
                app, # app from inner decorator
                args, # security parameters like allowed users or roles to pass into security method
                kwargs # security parameters like allowed users or roles to pass into security method
            )
    return gen_auth