import dash_core_components as dcc
from dash import html
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
import dash_bootstrap_components as dbc
import ee

from apiConfig.eeAuth import credentials
# ee.Authenticate()
ee.Initialize(credentials)

from client.constants import CITY_CONFIGS
from client.callbacks import *
from client.layouts import layout   
from client.app import app
# logging.basicConfig(
#     stream=sys.stdout, 
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
#     datefmt="%m/%d/%Y %H:%M:%S",
#     )

# logger = logging.getLogger(__name__)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    layout
])
server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)