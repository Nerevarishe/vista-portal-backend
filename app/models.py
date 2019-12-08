from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import Document
from mongoengine import fields as fl


class VistaApiDocument(Document):
    @staticmethod
    def get_all_fields(document_class, search_query: str):

        """ Return all user defined fields from model class object
         fields - must be Class
         search_query - string - prefix for fields in class"""

        model_fields = []
        for field in dir(document_class):
            if field[:len(search_query)] == search_query:
                model_fields.append(field)
        return model_fields

    @staticmethod
    def get_current_date():
        return (datetime.utcnow()).date()

    date_created = fl.DateTimeField(default=datetime.utcnow)
    date_edited = fl.DateTimeField(default=datetime.utcnow)

    meta = {'allow_inheritance': True}


class User(VistaApiDocument):
    username = fl.StringField(max_length=20, required=True, unique=True)
    # ip4_address = fl.StringField(max_length=15, required=True) # indexed
    password_hash = fl.StringField(max_length=94, required=True)
    refresh_token = fl.StringField()

    # TODO: change hashing!
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def fields(self):
    #     """
    #
    #     :return:
    #     """
    #     return self.get_all_fields(User, '')

# class TokenBlackList(Document):
#     jti = fl.StringField(max_length=36)
#     token_type = fl.StringField(max_length=10)
#     user_identity = fl.StringField(max_length=50)
#     revoked = fl.BooleanField()
#     expires = fl.DateTimeField()


class NewsPost(VistaApiDocument):
    post_body = fl.StringField()
    # author = fl.ReferenceField(User)


class DefecturaCard(VistaApiDocument):
    drug_name = fl.StringField(max_length=60)
    comment = fl.StringField(max_length=200)
    employee_name = fl.StringField(max_length=30)
    in_zd = fl.BooleanField(default=False) # indexed
    date = fl.DateField(default=VistaApiDocument.get_current_date) # indexed
    # user = fl.ReferenceField(User)

    # def fields(self):
    #     return self.get_all_fields(ServiceCenter, 'sc')
