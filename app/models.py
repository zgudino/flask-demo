from datetime import datetime
from flask import json
from mongoengine import ValidationError
from app import db
from mongoengine_goodjson import Document


class Model:
    def data(self):
        return json.loads(self.to_json())


class Author(Document):
    username = db.StringField(max_length=32, required=True)
    email = db.EmailField(default=None)
    name = db.StringField(default=None)

    @property
    def json(self):
        return json.loads(self.to_json())

    meta = {'collection': 'authors'}

    def clean(self):
        if Author.objects(email=self.email).count() > 0:
            raise ValidationError('(Error) Documento ya existe.')
            abort(500)


class Book(Document):
    author = db.ReferenceField(Author, reverse_delete_rule=2)
    title = db.StringField(required=True)
    published_on = db.DateTimeField(default=datetime.utcnow())

    @property
    def json(self):
        return json.loads(self.to_json())

    meta = {'collection': 'books'}
