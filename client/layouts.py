from dash import html
import dash_bootstrap_components as dbc
from dash import dcc

from .components.filters import filters
from .components.mapContainer import mapContainer
from .components.sdgCharts import sdgCharts
from .components.sdgTable import sdgTable
from .components.menu import menubar
from .constants import CITIES


filterSDG = html.Div([
    dcc.RadioItems(
        id="select-all-city",
        options=[
            {"label": "All", "value": "all"},
            {"label": "6", "value": "custom"},
        ],
        value="productive",
        labelStyle={"display": "inline-block"},
        className="dcc_control",
    ),
    dcc.Dropdown(
        id="city-dropdown-select",
        options=[{'label':c, 'value': c} for c in CITIES],
        multi=True,
        value=['Detroit', 'Dubai', 'Rio de Janeiro'],#, 'Mumbai', 'Nouakchott', 'Mexico City', 'Beijing', 'Dar Es Salaam', 'Lagos', 'Stockholm', 'Karachi', 'Charleston', 'Guangzhou', 'Tianjin', 'Cairo', 'Nairobi', 'La Paz', 'Shanghai', 'Kigali', 'Islamabad', 'New York'],
        className="dcc_control",
    ),
])

layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Location(id='redirect', refresh=True),
    menubar, 
    dbc.Row([
        dbc.Col(filters, md=4),
        dbc.Col(mapContainer,md=8),
    ]),
    dbc.Row([sdgTable]),
    dbc.Row([filterSDG]),
    dbc.Row([sdgCharts])
])
