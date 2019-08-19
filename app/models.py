from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import Document
from mongoengine import fields as fl


def get_current_date():
    utc_now = datetime.utcnow()
    return utc_now.date()


def get_all_fields(fields, search_query: str):

    """ Return all user defined fields from model class object
     fields - must be dir(MyClass)
     search_query - string - prefix for fields in class"""

    model_fields = []
    for field in fields:
        if field[:len(search_query)] == search_query:
            model_fields.append(field)
    return model_fields


class User(Document):
    username = fl.StringField(max_length=20)
    ip4_address = fl.StringField(max_length=15, required=True) # indexed
    password_hash = fl.StringField()
    refresh_token = fl.StringField()
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
    date = fl.DateField(default=get_current_date) # indexed
    # user = fl.ReferenceField(User)
    date_created = fl.DateTimeField(default=datetime.utcnow)
    date_edited = fl.DateTimeField(default=datetime.utcnow)


class Drugstore(Document):
    ds_name = fl.StringField(max_length=50)
    ds_address = fl.StringField(max_length=200)
    ds_worktime = fl.StringField(max_length=11)
    ds_phone = fl.StringField(max_length=16)
    ds_ip_phone = fl.StringField(max_length=4)

    def fields(self):
        return [self.ds_name, self.ds_address, ]


class ServiceCenterList(Document):
    sc_brands = fl.StringField(max_length=20)
    sc_address = fl.StringField(max_length=50)
    sc_phone = fl.StringField(max_length=16)


# class DeferredDrug(Document):
#     drug_name = fl.StringField(max_length=60) # indexed
#     drug_amount = fl.IntField(max_value=100)
#     comment = fl.StringField(max_length=200)
#     date_created = fl.DateTimeField(default=datetime.utcnow)
#     date_edited = fl.DateTimeField(default=datetime.utcnow)
