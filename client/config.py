import os
import json
import ee
import firebase_admin


""" Google Earth Engine Service Account Auth """
PRIVATE_KEY = os.environ['PRIVATE_KEY']
SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT')
credentials = ee.ServiceAccountCredentials(SERVICE_ACCOUNT, key_data=PRIVATE_KEY)


""" Firebase Configuration """
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
SERVICE_ACCOUNT_KEY = os.environ.get('SERVICE_ACCOUNT_KEY')
cred_obj = firebase_admin.credentials.Certificate(json.loads(SERVICE_ACCOUNT_KEY))


""" Mapbox Access Token """
MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN')