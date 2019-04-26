from flask_restplus import fields

from src.python.api.restplus import api

NewDatabaseApiModel = api.model('NewDatabaseApiModel', {
    "name": fields.String(required=True, description='Database name')
})

DatabaseApiModel = api.inherit('DatabaseApiModel', NewDatabaseApiModel, {
    "created_at": fields.DateTime(required=True, description='Date of creation'),
    "last_trained_at": fields.DateTime(required=False, description='Date of last training'),
    "updated_at": fields.DateTime(required=True, description='Date of last update'),
    "size": fields.Integer(required=True, description='Number of vectors')
})