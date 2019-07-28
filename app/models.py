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
