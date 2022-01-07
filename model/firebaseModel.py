import firebase_admin
from firebase_admin import firestore

class FirestoreModel:
    def __init__(self, configPath):
        cred_obj = firebase_admin.credentials.Certificate(configPath)
        default_app = firebase_admin.initialize_app(cred_obj)
        self.db = firestore.client(default_app)


    def get_all_data(self):
        ref = self.db.collection('sdg-records').stream()
        return [doc.to_dict() for doc in ref]

