
from dashify import Dash # Extended Dash class from the dashify package 
import dash_html_components as html

# New example Dash app
MinimalDashApp = Dash(__name__)

# Simple layout
MinimalDashApp.layout = html.Div(children=[
    html.H1("This is a dash app!"),
    html.P("Hello, from the dash app :)")
])

# run server if script is run directly
if __name__ == '__main__':
    MinimalDashApp.run_server(debug=True)


