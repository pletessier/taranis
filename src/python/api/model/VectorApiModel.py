from flask_restplus import fields

from src.python.api.restplus import api

VectorModel = api.model('VectorModel', {
    "id": fields.String(required=True, description='Vector id'),
    "data": fields.List(fields.Float, required=True, description='Data'),
    "metadata": fields.Raw(required=True, description='Metadata')
})

VectorListModel = api.model('VectorListModel', {
    'vectors': fields.List(fields.Nested(VectorModel)),
})
