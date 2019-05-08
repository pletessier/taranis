#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask_restplus import Resource, abort
from flask_restplus._http import HTTPStatus

from api.model.IndexModel import IndexModel
from service.taranis_service import TaranisService
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/<string:db_name>/index/<string:index_name>')
class IndexResource(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.db_service = TaranisService()

    @ns_db.doc('get_index')
    @api.marshal_with(IndexModel.IndexModel, code=HTTPStatus.OK)
    @ns_db.response(HTTPStatus.NOT_FOUND, 'Index not found')
    @ns_db.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def get(self, db_name, index_name):
        """Get an index"""
        return self.db_service.get_index(db_name, index_name)

    @ns_db.doc('delete_index')
    # @api.marshal_with(IndexModel.IndexCreationModel, code=HTTPStatus.OK)
    @ns_db.response(HTTPStatus.OK, 'Index deleted')
    @ns_db.response(HTTPStatus.NOT_FOUND, 'Index not found')
    @ns_db.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def delete(self, db_name, index_name):
        """Delete an index"""
        self.db_service.delete_index(db_name, index_name)
