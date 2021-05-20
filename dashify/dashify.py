from dash.dependencies import Input, Output
from dash import Dash
from flask import Flask
import dash_html_components as html


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
            dash_app.change_flask_server(app, url) # change flask server and init new url
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

def DashifySecure(secure_method):
    """Make dash app secure with own security method. Accepts an method to check for security.
    Dash app layout gets inititated with an security Div where the content is put in
    Callback checks on runtime if security method is matched
    If security method returns not True, an "Unauthorized" message appears

    Parameters
    ----------
    secure_method : function
        own security function
    """
    def secure(app:Dash, *args, **kwargs):

        # security Div where whole app.layout is put into
        app.layout = html.Div(children=app.layout, id="security-div")

        # callback to check on initilization if user is authorized
        @app.callback(
            Output("security-div", "children"),
            Input("security-div", "children")
        )
        def security(children):
            if secure_method(*args, **kwargs) == True:
                return children
            else:
                return "NOT AUTHORIZED"

    return secure
    



