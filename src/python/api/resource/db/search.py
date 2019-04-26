#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from flask_restplus import Resource
from flask_restplus._http import HTTPStatus

from api.model.VectorApiModel import VectorApiModel
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/<string:db_name>/search')
class SearchResource(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    @ns_db.doc('get_db')
    @ns_db.expect(VectorApiModel)
    @api.marshal_with(VectorApiModel, as_list=True, code=HTTPStatus.OK)
    @ns_db.response(HTTPStatus.NOT_FOUND, 'Database not found')
    @ns_db.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def post(self, db_name):
        '''
        Search a vector in the database
        '''
        vector = None
        return vector
