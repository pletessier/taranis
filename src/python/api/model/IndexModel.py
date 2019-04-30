from enum import Enum

from flask_restplus import fields

from api.model.json_serializable import JsonClassSerializable
from src.python.api.restplus import api


class IndexModel(JsonClassSerializable):

    class States(Enum):
        CREATED = "CREATED"
        TRAINED = "TRAINED"

    IndexCreationModel = api.model('IndexCreationModel', {
        'name': fields.String(required=True, description='Index name'),
        "config": fields.String(required=True, description='Index config')
    })

    IndexModel = api.inherit('IndexModel', IndexCreationModel, {
        "db_name": fields.String(required=True, description='Name of database'),
        "created_at": fields.DateTime(required=True, description='Date of creation'),
        "last_trained_at": fields.DateTime(required=False, description='Date of last training'),
        "updated_at": fields.DateTime(required=True, description='Date of last update'),
        "size": fields.Integer(required=True, description='Number of vectors'),
        "state": fields.String(required=True, description='Index state', enum=list(States.__members__.keys()))
    })

    serializables = ["name", "config", "db_name", "created_at", "last_trained_at", "updated_at", "size", "state"]

    def __init__(self, *initial_data, **kwargs):
        self.name = None
        self.config = None
        self.db_name = None
        self.created_at = None
        self.last_trained_at = None
        self.updated_at = None
        self.size = None
        self.state = str()

        super().__init__(*initial_data, **kwargs)
