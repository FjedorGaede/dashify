# - Import Flask - #
# from dashify.dashify import DashifySecure
from flask import Flask, redirect

# - Import Dashify - #
from dashify import Dashify, DashifySecure, dash_secure


# - Import Standalone Dash apps - # 
from dash_apps.minimal_dash import MinimalDashApp
from dash_apps.dash_visualization import app as InteractiveVisualApp
from dash_apps.secret_app import app as SecretDashApp

# - Import from Security Backend - #
from security_backend import get_current_user, security_method


""" 
This is a Flask app that is extended by importing dash apps and assigning them to a certain route. This example illustrates how to set up a route for a dash app and how to secure it with a decorator and security methods.
"""

# Create new Flask app
app = Flask(__name__)

# Dashify the Flask app
Dashify(app)

# Index of Flask app
@app.route('/')
def index():
    return """
    <h1>Flask says hello</h1>
    <p><a href='/minimal_dash'>Minimal Dash Example</a></p>
    <p><a href='/interactive_visualization'>Interactive Visualization Dash Example</a></p>
    <p><a href='/secured/dash_app'>A secret dash</a></p>
    """

# Minimal example imported Dash App
@app.dash_route('/minimal_dash')
def dash_app():
    return MinimalDashApp


# Setup security functionality by using the provided methods of the security backend. This adds the possibility to use a decorator that checks if the secure_method returns True or False. This changes the global behaviour of the `dash_secure` decorator.
DashifySecure(secure_method = security_method)


# Secured Dash App by using the security backend 
@dash_secure(allowed_users = ['Mariah']) # Change the list of users here to allow access (In this case the current user it checks access for is called 'Alex')
@app.dash_route('/secured/dash_app')
def dash_app():
    return SecretDashApp


# To change the access method for a certain app one can also define another `access_denied_behavior` and security method. These can then be inserted in a certain `dash_secure` decorator for only using this access method in that case. 
def access_denied_behavior():
    return redirect('/')

def dumbsecmethod():
    return True

# Interactive Visualization Dash app that is secured with a custom secure_method and also has a custom access denied behavior.
@dash_secure(secure_method = dumbsecmethod, access_denied_behavior=access_denied_behavior)
@app.dash_route('/interactive_visualization')
def visualization_app():
    return InteractiveVisualApp

if __name__ == '__main__':
    app.run(debug=True,port = 5006)


