from flask_restplus import fields

from src.python.api.restplus import api


IndexModelApiModel = api.model('IndexModelApiModel', {
    "data": fields.Raw(required=True, description='IndexModel data')
})

