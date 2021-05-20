# Dashify
Package includes dash application into flask app by using syntax very near to flask itself.

# Basic Usage

## Dash
``` python
# For using dashify, you need to use the dash class from Dashify
from dashify import Dash

# Build you Dash application 
SomeDashApp = Dash(__name__)

# Simple layout
SomeDashApp.layout = html.Div(children=[
    html.P("Dash says Hello")
])

# Build callbacks
# ...
```

## Flask
```python
# You need to dashify your flask application by using this line in your flask code:
Dashify(app)

# Then you are able to append the dash app with a given url to the flask app
@app.dash_route('/dash_app')
def dash_app():
    return SomeDashApp
```