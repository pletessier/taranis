from flask_restplus import fields

from src.python.api.restplus import api

VectorDataModel = api.model('VectorDataModel', {
    "data": fields.List(fields.Float, required=True, description='Data')
})

VectorDataListModel = api.model('VectorDataListModel', {
    'vectors': fields.List(fields.Nested(VectorDataModel)),
})

VectorModel = api.model('VectorModel', {
    "id": fields.String(required=True, description='Vector id'),
    "data": fields.List(fields.Float, required=True, description='Data'),
    "metadata": fields.Raw(required=True, description='Metadata')
})

VectorListModel = api.model('VectorListModel', {
    'vectors': fields.List(fields.Nested(VectorModel)),
})
