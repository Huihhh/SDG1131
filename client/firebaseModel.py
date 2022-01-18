import firebase_admin
from firebase_admin import firestore
from firebase_admin import auth

class FirestoreModel:
    def __init__(self, db):
        self.db = db


    def get_all_data(self, uid):
        ref = self.db.collection('sdg-records').stream()
        return [doc.to_dict() for doc in ref]
    

    

    
    

