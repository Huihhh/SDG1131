import pandas as pd
import firebase_admin
from firebase_admin import firestore

from .config import cred_obj

# Firebase app
default_app = firebase_admin.initialize_app(cred_obj)

def get_db():
    return firestore.client(default_app)


