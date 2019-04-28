from datetime import datetime

from flask_restplus import fields

from api.model.json_serializable import JsonClassSerializable
from src.python.api.restplus import api

CreationModel = api.model('CreationModel', {
    "name": fields.String(required=True, description='Database name')
})

Model = api.inherit('Model', CreationModel, {
    "created_at": fields.DateTime(required=True, description='Date of creation'),
    "last_trained_at": fields.DateTime(required=False, description='Date of last training'),
    "updated_at": fields.DateTime(required=True, description='Date of last update'),
    "size": fields.Integer(required=True, description='Number of vectors')
})


class DatabaseModel(JsonClassSerializable):
    serializables = ["name", "created_at", "last_trained_at", "updated_at", "size"]

    def __init__(self, *initial_data, **kwargs):
        self.name = None
        self.created_at = None
        self.last_trained_at = None
        self.updated_at = None
        self.size = None

        super().__init__(*initial_data, **kwargs)
