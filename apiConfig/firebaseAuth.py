import firebase_admin
import os
import json

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
SERVICE_ACCOUNT_KEY = os.environ.get('SERVICE_ACCOUNT_KEY')
cred_obj = firebase_admin.credentials.Certificate(json.loads(SERVICE_ACCOUNT_KEY))