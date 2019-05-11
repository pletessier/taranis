#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask_restplus import Resource, abort
from flask_restplus._http import HTTPStatus

from api.model.IndexModelApiModel import IndexModelApiModel
from service.taranis_service import TaranisService
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/<string:db_name>/index/<string:index_name>/model')
class IndexModelResource(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.db_service = TaranisService()

    @ns_db.doc('get_index_model')
    @api.marshal_with(IndexModelApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'IndexModel not found')
    @ns_db.response(500, 'Internal server error')
    def get(self, db_name):
        """Get the index model"""
        abort(HTTPStatus.NOT_IMPLEMENTED)

    @ns_db.doc('delete_index_model')
    @api.marshal_with(IndexModelApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'IndexModel not found')
    @ns_db.response(500, 'Internal server error')
    def delete(self, db_name):
        """Delete the index model"""
        abort(HTTPStatus.NOT_IMPLEMENTED)

    @ns_db.doc('put_index_model')
    @ns_db.expect(IndexModelApiModel)
    @api.marshal_with(IndexModelApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'IndexModel not found')
    @ns_db.response(500, 'Internal server error')
    def put(self, db_name):
        """Set the index model"""
        abort(HTTPStatus.NOT_IMPLEMENTED)

    @ns_db.doc('post_index_model')
    @ns_db.response(HTTPStatus.OK, 'Index has been trained')
    @ns_db.response(404, 'IndexModel not found')
    @ns_db.response(500, 'Internal server error')
    def post(self, db_name, index_name):
        """Train the index model"""
        self.db_service.train_index(db_name, index_name)

