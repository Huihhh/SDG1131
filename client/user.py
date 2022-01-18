from flask_login import UserMixin
from .db import get_db


class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        db = get_db()
        user_ref = db.collection(u'users').document(user_id).get()
        if not user_ref.exists:
            return None
        user_ref = user_ref.to_dict()
        user = User(
            id_=user_id, name=user_ref['name'], email=user_ref['email'], profile_pic=user_ref['profile_pic']
        )
        return user
    
    @staticmethod
    def get_records(uid):
        db = get_db()
        ref = db.collection('users').document(uid).collection('sdg-records').stream()
        return [doc.to_dict() for doc in ref]

    @staticmethod
    def add_record(uid, doc_name, data):
        db = get_db()
        db.collection('users').document(uid).collection('sdg-records').document(doc_name).set(data)

    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        db.collection(u'users').document(id_).set({
            u'name': name,
            'email': email,
            'profile_pic': profile_pic
        })