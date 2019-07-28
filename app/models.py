from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import Document
from mongoengine import fields as fl


class User(Document):
    username = fl.StringField(max_length=20)
    ip4_address = fl.StringField(max_length=15, required=True) # indexed
    password_hash = fl.StringField()
    date_created = fl.DateTimeField(default=datetime.utcnow)
    date_edited = fl.DateTimeField(default=datetime.utcnow)

    # TODO: change hashing!
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# class TokenBlackList(Document):
#     jti = fl.StringField(max_length=36)
#     token_type = fl.StringField(max_length=10)
#     user_identity = fl.StringField(max_length=50)
#     revoked = fl.BooleanField()
#     expires = fl.DateTimeField()


class NewsPost(Document):
    post_body = fl.StringField()
    author = fl.ReferenceField(User)
    date_created = fl.DateTimeField(default=datetime.utcnow) # indexed
    date_edited = fl.DateTimeField(default=datetime.utcnow)


class DefecturaCard(Document):
    drug_name = fl.StringField(max_length=60)
    comment = fl.StringField(max_length=200)
    employee_name = fl.StringField(max_length=30)
    in_zd = fl.BooleanField(default=False) # indexed
    date = fl.DateField() # indexed
    user = fl.ReferenceField(User)
    date_created = fl.DateTimeField(default=datetime.utcnow)
    date_edited = fl.DateTimeField(default=datetime.utcnow)


class DeferredDrug(Document):
    drug_name = fl.StringField(max_length=60) # indexed
    drug_amount = fl.IntField(max_value=100)
    comment = fl.StringField(max_length=200)
    date_created = fl.DateTimeField(default=datetime.utcnow)
    date_edited = fl.DateTimeField(default=datetime.utcnow)