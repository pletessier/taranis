from flask_restplus import fields

from src.python.api.restplus import api

VectorApiModel = api.model('VectorApiModel', {
    "id": fields.String(required=True, description='Vector id'),
    "data": fields.Raw(required=True, description='Data'),
    "metadata": fields.Raw(required=True, description='Metadata')
})