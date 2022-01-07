# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash_extensions.enrich import Dash
import dash_bootstrap_components as dbc
import ee

from apiConfig.eeAuth import credentials
# ee.Authenticate()
ee.Initialize(credentials)

from client.constants import CITY_CONFIGS
# logging.basicConfig(
#     stream=sys.stdout, 
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
#     datefmt="%m/%d/%Y %H:%M:%S",
#     )

# logger = logging.getLogger(__name__)


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], external_scripts=["https://unpkg.com/feather-icons"], title='SDG 11.3.1')

