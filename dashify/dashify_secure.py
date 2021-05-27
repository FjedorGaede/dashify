import flask
from dash_auth import BasicAuth
from dash_auth.basic_auth import Auth
from six import iteritems
import types

# Exceptions
class SecurityMethodNotFound(Exception):
    pass

class NotAFunction(Exception):
    pass

# Modification of class Auth
# We have no access to the initialization of the Auth method hence we have to overwrite this method for our needs
def _protect_views(self):
    """Method of class Auth.
    Needs to be modified to only change views of dash application in flask server. Super class method overwrites all view functions in flask server object, also non-dash ones.
    """
    # Only views that are from dash app and not flask views / routes
    views_dash_app = [view_name for view_name, view_method in self.app.server.view_functions.items() \
        if view_name.startswith(self._index_view_name)]
    
    # go through view_functions and overwrite view_functions if from dash app and not index
    for view_name, view_method in iteritems(
                self.app.server.view_functions):
            # check for view name: Needs to be in above list
            if view_name in views_dash_app and view_name != self._index_view_name:
                self.app.server.view_functions[view_name] = \
                    self.auth_wrapper(view_method)

# Overwrites _protect_views method of class Auth
Auth._protect_views = _protect_views

# Customized BasicAuth class
class DashifyAuth(BasicAuth):
    """customized Auth class. Modifies all functions except login_request which isn't used

    Parameters
    ----------
    BasicAuth : Auth
        Class BasicAuth 
    """
    def __init__(self, app, secure_method = None,  access_denied_behavior = None, *args, **kwargs):
        """initializes DashifyAuth with dash app, security method if set and arguments that should get passed into security method.
        Methods for behavior at view loading.

        Parameters
        ----------
        app : Dash
            dash application which should made secure
        secure_method : function, optional
            custom security method (can get set by using method DashifySecure), by default None
        access_denied_behavior : function, optional
            custom behavior when access denied method (can get set also  by using method DashifySecure), by default None
        args, kwargs
            arguments for security method
        """
        # initialize Auth object for dash app
        Auth.__init__(self, app, _overwrite_index = True)
        
        # overwrite secure method if set
        if secure_method != None:
            # raise error if secure method not a function
            if type(self.secure_method) != types.FunctionType:
                raise NotAFunction
            self.secure_method = secure_method
        
        # overwrite access denied behavior function if set
        if access_denied_behavior != None:
            # raise error if access denied behavior not a function
            if type(access_denied_behavior) != types.FunctionType:
                raise NotAFunction
            self.access_denied_behavior = access_denied_behavior
        
        # write args and kwargs into object for passing into secure method
        self.args = args
        self.kwargs = kwargs

    def is_authorized(self) -> bool:
        """executes secure method and returns result. Executed when opening dash view

        Returns
        -------
        bool
            result of secure check
        """
        return self.secure_method(*self.args, **self.kwargs)

    def auth_wrapper(self, f):
        """wrapper for dash views which are not the index that checks for authorization

        Parameters
        ----------
        f : FunctionType
            view function
        """
        def wrap(*args, **kwargs):
            if not self.is_authorized():
                return self.access_denied_behavior()

            response = f(*args, **kwargs)
            return response
        return wrap

    def index_auth_wrapper(self, original_index):
        """wrapper for index of wrap function that checks for authorization

        Parameters
        ----------
        original_index : FunctionType
            view function of index
        """
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.access_denied_behavior()
                
        return wrap

    @staticmethod
    def secure_method(*args, **kwargs):
        """security method. has to be defined!

        Raises
        ------
        SecurityMethodNotFound
            Exception because own method should be defined
        """
        raise SecurityMethodNotFound

    @staticmethod
    def access_denied_behavior():
        """Behavior in case that access is denied.
        Default: Response 403
        Can get modified in decorator / when instantiating auth object

        Returns
        -------
        Response
            403
        """
        return flask.Response(status=403)

def DashifySecure(secure_method = None, access_denied_behavior = None):
    """Bounds secure method and access denied behavior method to DashifyAuth class globally. Can be also set when using decorator dash_secure
    Usage:
        DashifySecure(secure_method = custom_secure_method, access_denied_behavior = access_denied_behavior)

    Parameters
    ----------
    secure_method : method
        secure_method to overwrite standard security method
    access_denied_behavior : method
        Behavior in case that access is denied.
    """
    
    # secure method can get set directly when instantiate object
    if secure_method != None:
        if type(secure_method) != types.FunctionType:
            # raise error if secure method not a function
            raise NotAFunction
        DashifyAuth.secure_method = staticmethod(secure_method)

    # overwrite access denied behavior function if set
    if access_denied_behavior != None:
        # raise error if access denied behavior not a function
        if type(access_denied_behavior) != types.FunctionType:
            raise NotAFunction
        DashifyAuth.access_denied_behavior = staticmethod(access_denied_behavior)


def dash_secure(secure_method = None  , access_denied_behavior = None, *args, **kwargs ):
    """Make dash app secure with own security method. Accepts an method to check for security and further parameters necessary for security method. 
    Behavior when access is denied can be set as well.
    Instantiates BasicAuth object for dash app.
    Important: Decorator Needs to be put above dash routing because Auth modifies view functions of flask server!
    Parameters
    ----------
    secure_method : function, optional
        custom security method (can get set by using method DashifySecure), by default None
    access_denied_behavior : function, optional
        custom behavior when access denied method (can get set also by using method DashifySecure), by default None
    """
    def gen_auth(app):
        """Generates the BasicAuth Object

        Parameters
        ----------
        app : Dash
            dash object
        """
        return DashifyAuth(
                app, # app from inner decorator
                secure_method,# security method
                access_denied_behavior, # function for access denied behavior, e. g. redirecting to index
                *args, # args for security method
                **kwargs, # kwargs for security method
            )
    return gen_auth