from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import sd_material_ui as dm 
from dash import dash_table

from ..constants import CITIES, CD_DATA, PG_DATA, BP_DATA, COLUMNS, ADMIN_LEVEL

YEARS = [1975, 1990, 2000, 2005, 2010, 2015]

filters = dm.Paper(
    zDepth=8,
    children = [
        html.H6(children='Select interested city'),
        dcc.Dropdown(
            id="city-single-select",
            options=[{'label':c, 'value': c} for c in CITIES],
            # multi=True,
            value='Mumbai',
            className="dcc_control",
        ),
        dm.Tooltip(
            dm.Button(id='draw-roi', n_clicks=0, children='Use drawn ROI', variant="outlined"),
            title="Make sure there are no city definitions left on the map!",
            # placement='right',
            # className="mx-5",
        ),
        dcc.RadioItems(
            id='adminlevel-radioItem',
            options=ADMIN_LEVEL,
            value='2',
        ),
        dm.Accordion(
            id='city-definition-accord',
            label = 'Get City Definition',
            square=True,
            children=[
                html.Div([
                    html.H6(children='Choose population data for city definition'),
                    dbc.Row([
                        dbc.Col(
                            dcc.RadioItems(
                                        id='pop4def-radioItem',
                                        options=[{'label': pop['name'], 'value':pop['name']} for pop in CD_DATA],
                                        value='GHS-Pop 1km',
                            ), md=9
                        ),
                        dbc.Col([
                            dm.Tooltip(
                                dcc.Link(html.P('More info'), href=pop['url']),
                                title=pop['info'],
                                
                            ) for pop in CD_DATA
                        ])
                    ]),

                    # ============= year filter ================
                    html.H6(children='Select year for city definition'),
                    dcc.Dropdown(
                        id="year-dropdown-select",
                        options=[ {'label': year, 'value': year} for year in YEARS],
                        # multi=True,
                        value=1990,
                        className="dcc_control",
                    ),  
                        # ================== Min & Max for visualization ========================
                    html.P('vis-min & vis-max'),
                    dbc.Row([
                        dbc.Col(dcc.Input(id='vis-min-state', type='number', value='300'), md=5),
                        dbc.Col(dcc.Input(id='vis-max-state', type='number', value='1500'), md=5),
                        dbc.Col(dm.Button(id='vis-param-state', n_clicks=0, children='Ok', variant="outlined"), md=2)
                    ]),
                    
                    # ================== cuttoff for urban cluster ========================
                    html.P('Cell TH & Cluster TH'),
                    dbc.Row([
                        dbc.Col(dcc.Input(id='cell-TH-state', type='number', value='300'), md=5),
                        dbc.Col(dcc.Input(id='cluster-TH-state', type='number', value='5000'), md=5),
                        dbc.Col(dm.Button(id='submit-button-state', n_clicks=0, children='Submit', variant="outlined"), md=2),
                    ]),    
                    # Expport city definition
                    dbc.Row([
                        dbc.Col([dm.Button(id='update-city-definition', n_clicks=0, children='Update City Definition', variant="outlined")]),
                        dbc.Col(dm.Snackbar(id='alert-update-status', message='', open=False))
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Dropdown(
                                id="export-option",
                                options=[{'label': 'Export to project asset', 'value': 'projAsset'},
                                        {'label': 'Export as geojson', 'value': 'geojson'}],
                                value='projAsset',
                                className="dcc_control",
                        ), md=7),
                        dbc.Col(dm.Button(id='export-city-definition', n_clicks=0, children='Export City Definition', variant="outlined")),
                        dbc.Col(dcc.Download(id="download-city-definition")),
                    ]),
                    dm.Snackbar(id='alert-export-status', message='', open=False)
                ])
            ]
        ),
        dm.Accordion(
            id='SDG-accord',
            label='Calculate SDG 11.3.1',
            square=True,
            children = [
                html.Div([
                    html.H6(children='Choose population data', style={'width': '14em'}),
                    dbc.Row([
                        dbc.Col(
                            dcc.RadioItems(
                                        id='pop-radioItem',
                                        options=[{'label': pop['name'], 'value':pop['name']} for pop in PG_DATA],
                                        value='GHS-Pop 250m'
                            ), md=9
                        ),
                        dbc.Col([
                            dm.Tooltip(
                                dcc.Link(html.P('More info'), href=pop['url']),
                                title=pop['info']
                            ) for pop in PG_DATA
                        ])
                    ]),

                    # dm.Button(id='compare-popdata', n_clicks=0, children='Compare above data', variant="outlined"),
                    html.H6(children='Choose built-up data'),
                    dbc.Row([
                        dbc.Col(
                            dcc.RadioItems(
                                        id='built-radioItem',
                                        options=[{'label': bp['name'], 'value':bp['name']} for bp in BP_DATA],
                                        value='GHS-Built 38m'
                            ),md=8
                        ),
                        dbc.Col([
                            dm.Tooltip(
                                dcc.Link(html.P('More info'), href=pop['url']),
                                title=pop['info']
                            ) for pop in BP_DATA
                        ])
                    ]),
                    dm.Button(id='compare-bpdata', n_clicks=0, children='Compare above data', variant="outlined"),
                    html.H6(children='Select start year'),
                    dbc.Row([
                        dbc.Col(                    
                            dcc.Dropdown(
                                id="start-year-select",
                                options=[ {'label': year, 'value': year} for year in YEARS],
                                # multi=True,
                                value=1990,
                                className="dcc_control",)
                        ),    
                        dbc.Col(dm.Button(id='compute-sdg', n_clicks=0, children='Compute', variant="outlined"),)
                    ]),
                    html.Div(id='sdg-res')
                ])
            ]
        ),
    ]
)
