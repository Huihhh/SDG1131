from dash import html
import dash_bootstrap_components as dbc
import sd_material_ui as dm 

menubar = dbc.NavbarSimple(
    # children=[
    #     dbc.NavItem(dbc.NavLink("Login with Google", href="/login", n_clicks=0)),
    #     dbc.NavItem(id='profile'),
    #     ],
    brand="SDG 11.3.1",
    brand_href="#",
    color="#595959",
    dark=True,
    fixed="top"
    )