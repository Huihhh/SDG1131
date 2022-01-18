from dash import dcc
from dash import html

from ..constants import COMPARE

sdgCharts = dcc.Tabs([
                dcc.Tab(label=comp['label'], children=[
                    *[dcc.RadioItems(id=comp['label'].replace(' ', '-') +key.replace(' ', '-'), 
                                    options=[{'label': v['name'], 'value': v['name']} for v in value],
                                    value=value[0]['name'],
                                    labelStyle={"display": "inline-block"},
                                    className="dcc_control",
                        ) for key, value in comp['radioItems'].items()
                    ],
                    html.Div(id='sdg-charts-container-' + comp['label'].replace(' ', '-'))
                ]) for comp in COMPARE
            ], id='res-tabs')