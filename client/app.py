# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import os
import flask
from dash_extensions.enrich import Dash
import dash_bootstrap_components as dbc
import ee
import json
# Third party libraries
from flask import Flask, redirect, request, url_for
from oauthlib.oauth2 import WebApplicationClient
import requests
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)


from .config import credentials, cred_obj, GOOGLE_CLIENT_ID, GOOGLE_DISCOVERY_URL, GOOGLE_CLIENT_SECRET
from .user import User
# ee.Authenticate()
ee.Initialize(credentials)

# Exposing the Flask Server to enable configuring it for logging in
server = flask.Flask(__name__)
server.config.update(SECRET_KEY=os.getenv('SECRET_KEY') or os.urandom(24))

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)
# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

app = Dash(__name__, 
    server=server,
    url_base_pathname='/',
    external_stylesheets=[dbc.themes.BOOTSTRAP], 
    external_scripts=["https://unpkg.com/feather-icons"], 
    title='SDG 11.3.1'
)

@server.route("/")
def index():
    return app.index()

@server.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    print(f'request_uri   {__name__}:', request_uri)
    return redirect(request_uri)


@server.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add to database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)


    # Send user back to homepage
    return redirect(url_for("index"))


@server.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
