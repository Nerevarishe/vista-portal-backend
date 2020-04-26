from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import Document
from mongoengine import fields as fl, EmbeddedDocument

SHIFT_START_TIME = (
    (730, '7:30'),
    (800, '8:00'),
    (830, '8:30'),
    (900, '9:00'),
    (1000, '10:00'),
    (0, '')
)


# TODO: Configure indexes
class VistaApiDocument(Document):

    meta = {
        'abstract': True
    }

    # @staticmethod
    # def get_all_fields(document_class, search_query: str):
    #
    #     """ Return all user defined fields from model class object
    #      fields - must be Class
    #      search_query - string - prefix for fields in class"""
    #
    #     model_fields = []
    #     for field in dir(document_class):
    #         if field[:len(search_query)] == search_query:
    #             model_fields.append(field)
    #     return model_fields
    #
    # @staticmethod
    # def get_current_date():
    #     return (datetime.utcnow()).date()

    date_created = fl.DateTimeField(default=datetime.utcnow)
    date_edited = fl.DateTimeField(default=datetime.utcnow)


class User(VistaApiDocument):
    username = fl.StringField(max_length=20, required=True, unique=True)
    ip4_address = fl.StringField(max_length=15, required=True)  # indexed
    password_hash = fl.StringField(max_length=94, required=True)
    refresh_token = fl.StringField()
    role = fl.StringField(max_length=20)

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
    author = fl.ReferenceField(User)


class DefecturaCard(VistaApiDocument):
    drug_name = fl.StringField(max_length=60, required=True)
    comment = fl.StringField(max_length=200)
    employee_name = fl.StringField(max_length=30, required=True)
    in_zd = fl.BooleanField(default=False)  # indexed
    date = fl.DateField(default=(datetime.utcnow()).date())  # indexed


class Employee(VistaApiDocument):

    class VacationDates(EmbeddedDocument):
        vacation_start_date = fl.DateField()
        vacation_end_date = fl.DateField()

    first_name = fl.StringField(max_length=30, required=True)
    last_name = fl.StringField(max_length=30, required=True)  # indexed
    patronymic = fl.StringField(max_length=30)
    active = fl.BooleanField(default=True)
    preffered_time = fl.IntField(max_value=1000, choices=SHIFT_START_TIME)
    start_work_date = fl.DateField(default=(datetime.utcnow()).date())
    date_of_dismissal = fl.DateField()
    vacation_days = fl.IntField(default=0)
    vacation_dates = fl.EmbeddedDocumentListField(VacationDates)


class Schedule(VistaApiDocument):
    employee = fl.ReferenceField(Employee)
    shift_start_time = fl.IntField(max_value=1000, choices=SHIFT_START_TIME, required=True)
    work_day = fl.DateField()  # indexed
    vacation_day = fl.DateField()
