# - Import Flask - #
from flask import Flask

# - Import Dashify - #
from dashify import Dashify, DashifySecure


# - Import Standalone Dash apps - # 
from dash_apps.minimal_dash import MinimalDashApp
from dash_apps.dash_visualization import app as InteractiveVisualApp
from dash_apps.secret_app import app as SecretDashApp

# - Import from Security Backend - #
from security_backend import get_current_user, security_method


""" 
This is a Flask app that is extended by importing dash apps.
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

# Normal Dash App
@app.dash_route('/minimal_dash')
def dash_app():
    return MinimalDashApp


# Setup security functionality by using the provided methods of the security backend
secure = DashifySecure(secure_method = security_method)


# Secured Dash App
@app.dash_route('/secured/dash_app')
def dash_app():
    secure(SecretDashApp, ["Mariah", "Peter"] )
    return SecretDashApp

# Interactive Visualization Dash app
@app.dash_route('/interactive_visualization')
def visualization_app():
    return InteractiveVisualApp



if __name__ == '__main__':
    app.run(debug=True,port = 5006)


