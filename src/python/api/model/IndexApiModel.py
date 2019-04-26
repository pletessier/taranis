from flask_restplus import fields

from src.python.api.restplus import api

NewIndexApiModel = api.model('NewIndexApiModel', {
    'name': fields.String(required=True, description='Index name'),
    "config": fields.String(required=True, description='Index config')
})

IndexApiModel = api.inherit('IndexApiModel', NewIndexApiModel, {
    "created_at": fields.DateTime(required=True, description='Date of creation'),
    "last_trained_at": fields.DateTime(required=False, description='Date of last training'),
    "updated_at": fields.DateTime(required=True, description='Date of last update'),
    "size": fields.Integer(required=True, description='Number of vectors'),
    "state": fields.String(required=True, description='Index state', enum=["CREATED", "TRAINED"])
})

