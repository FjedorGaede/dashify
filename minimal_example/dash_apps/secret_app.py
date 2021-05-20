
from dashify import Dash # Extended Dash class from the dashify package 
import dash_html_components as html

# New example Dash app
app = Dash(__name__)

# Simple layout
app.layout = html.Div(children=[
    html.H1("Secret Information"),
    html.P("Psst this is secret!")
])

# run server if script is run directly
if __name__ == '__main__':
    app.run_server(debug=True)


