# Dashify
Dashify integrates your Dash applications into your Flask app by using easy syntax which are close to the Flask syntax. Additionally, it provides security funtionality for your Dash app.

# Usage of Dashify
The general usage of Dashify is described below. It is assumed that each Dash app is provided in a separate file and are imported in the main file the Flask app is created in. For a minimal example check the [Minimal Example](minimal_example) directory.
## Dash
When creating a Dash app you do not have to change any syntax or add additional methods or parameters. You just write your Dash app as you always do. It is also possible to test the Dash app "locally" in the file you are creating it before importing it to the Flask app. See the example below.
``` python
# some_dash_app.py
# Importing Dash from dash
from dash import Dash

# Build you Dash application 
SomeDashApp = Dash(__name__)

# Build layout
SomeDashApp.layout = html.Div(...)

# Build callbacks
SomeDashApp.callback(...)
def callback(...):
    return output
    
# Test the app 'locally' without Flask providing your Flask app.
if __name__ == '__main__':
    SomeDashApp.run_server(debug=True)
```
## Flask
```python
from flask import Flask
app = Flask(__name__)
# flask configuration and flask routes...

from dashify import Dashify, dash_route
# You need to dashify your flask application by using this line in your flask code:
Dashify(app)

# Import dash app
from some_dash_app import SomeDashApp

# Then you are able to append the dash app with a given url route to the flask app
@app.dash_route('/dash_app')
def dash_app():
    """ 
    Here you can do something with the dash application in case you need some values of the flask app configuration. 
    Note: When using the decorator, the flask app server of the dash application is changed from a temporary one to your flask application.
    """
    return SomeDashApp
```
# Usage of Dashify Security
Dashify provides a decorator which you can use to have an authentication check when a user opens the dash app. The authentication is based on BasicAuth from [dash_auth](https://github.com/plotly/dash-auth).
Assuming that there already exists an authentication method in your environment (e. g. you are checking that a user is in a certain user group), you just have to pass this into the security mechanism of Dashify. You can also define a function with the behavior that should appearing when the access is denied.

Notes:
- You have to define a security method that returns a boolean after checking for access rights
- Default behavior if access is denied: Response of 403
### Define own security method
```python
# Checks if the "current" user is in a certain list of user names.
def security_method(allowed_users):
    if get_current_user() in allowed_users:
        return True 
    else:
        return False
```
Note: The return value has to be a boolean.
### Define own access denied behavior
```python
def access_denied_behavior():
    return flask.redirect('/') 
```
Note: The return value has to be either a flask template or redirection
### Integrate dash security into your app
You can integrate security by using `DashifySecure` and providing a method to check for access rights for the argument `secure_method`. This enables us to use the decorator `@dash_secure` above the `@app.dash_route`. It takes in all the arguments and keyword arguments of your security method. In this case this is the `allowed_users` list. 
```python
from flask import Flask
app = Flask(__name__)
# flask configuration and flask routes...

from dashify import Dashify, dash_route
# You need to dashify your flask application by using this line in your flask code:
Dashify(app)

# Import dash app
from some_dash_app import SomeDashApp

# Enable the security functionality 
DashifySecure(
        secure_method = security_method, 
        access_denied_behavior = user_defined_access_denied_behavior
        )

# You can also use different key value arguments here that are matching your security method
@dash_secure(allowed_users = ['Alex']) 
@app.dash_route('/dash_app')
def dash_app():
    return SomeDashApp
```
As we can see above we globally provide a security method by using `DashifySecure(secure_method = security_method)`. Additionally, it is possible to provide the security and access denied methods for a single dash application route by adding passing them into the `@dash_secure` decorator as you can see in the example below.
```python
from flask import Flask
app = Flask(__name__)
# flask configuration and flask routes...

from dashify import Dashify, dash_route, dash_secure
Dashify(app)

@dash_secure(secure_method = security_method,
    access_denied_behavior = user_defined_access_denied_behavior,
    allowed_users = ['Alex'])
@app.dash_route('/dash_app')
def dash_app():
    return SomeDashApp
```
