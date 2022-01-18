import pandas as pd
import firebase_admin
from firebase_admin import firestore

from config import cred_obj

def read_gspread(sheet_id, sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    return pd.read_csv(url)


# SDG dataframe
df = read_gspread(sheet_id = '1AmMWSf3tcgVofAGqH0H0jJVWLSnnX2A60RFzvJlYXgU', sheet_name = 'SDG11.3.1_Calculations')
df = df.round(3)

# Firebase app
default_app = firebase_admin.initialize_app(cred_obj)

def get_db():
    return firestore.client(default_app)


