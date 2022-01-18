import os
import dash
import json

from dash_extensions.enrich import Output, Input, State, ServersideOutput

from flask_login import current_user

from ..app import app

@app.callback(
    Output('redirect', 'href'),
    Input('profile', 'pathname')
)
def login(pathname):
    url = '/'
    return url