# Dashify
Dashify integrates your Dash applications into your Flask app by using easy syntax very near to Flask itself. Additionally, it provides security funtionality for your Dash app.

# Usage of Dashify
The general usage of Dashify is described below. The creation of the dash app is similar with dash itself, except you should import Dash from dashify.
## Dash
``` python
# For using dashify, you need to use the dash class from Dashify
from dashify import Dash

# Build you Dash application 
SomeDashApp = Dash(__name__)

# Build layout
SomeDashApp.layout = html.Div(...)

# Build callbacks
SomeDashApp.callback(...)
def callback(...):
    return output
```

## Flask
```python
# You need to dashify your flask application by using this line in your flask code:
Dashify(app)

# Then you are able to append the dash app with a given url to the flask app
@app.dash_route('/dash_app')
def dash_app():
    # here you can do something with the dash application in case you need some values of the flask app configuration. Note: When using the decorator, the flask app server of the dash application is changed from a temporary one to your flask application.
    return SomeDashApp
```

# Usage of Dashify Security
Dashify provides a decorator which you can use to have an authentication check when a user opens the dash app. The authentication is based on BasicAuth from Dash itself.
Assuming that there exists already an authentication method in your environment (e. g. you are checking a users group on being matched), you just have to pass this into the security mechanism of dashify. You can also define a function with the behavior that should appearing when the access is denied.
Notes:
- You have to define an own security method
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
### Integrate security it into your app
You can integrate security by using the decorator dash_secure above the dash_route-decorator.
```python
@dash_secure(allowed_users = ['Alex']) # You can also use different key value arguments here that are matching your security method
@app.dash_route('/dash_app')
def dash_app():
    return SomeDashApp
```
You can set up the security method and access denied behavior either globally for all dash applications or only for one dash application
Globally set up the methods:
```python
DashifySecure(secure_method = security_method, access_denied_behavior = user_defined_access_denied_behavior)
```

You can also pass the methods into the decorator dash_secure, this is only done for one Dash app:
```python
@dash_secure(secure_method = security_method,
    access_denied_behavior = user_defined_access_denied_behavior,
    allowed_users = ['Alex'])
@app.dash_route('/dash_app')
def dash_app():
    return SomeDashApp
```