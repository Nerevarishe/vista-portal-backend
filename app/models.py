from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db


class User(db.Document):
    username = db.StringField(max_length=20)
    ip4_address = db.StringField(max_length=15, required=True)
    password_hash = db.StringField()
    date_created = db.DateTimeField(default=datetime.utcnow)
    date_edited = db.DateTimeField(default=datetime.utcnow)

    # TODO: change hashing!
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class NewsPost(db.Document):
    post_body = db.StringField()
    author = db.ReferenceField(User)
    date_created = db.DateTimeField(default=datetime.utcnow)
    date_edited = db.DateTimeField(default=datetime.utcnow)