#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask_restplus import Resource, abort
from flask_restplus._http import HTTPStatus

from api.model.IndexApiModel import IndexApiModel, NewIndexApiModel
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/<string:db_name>/index/<string:index_name>')
class IndexResource(Resource):

    @ns_db.doc('get_index')
    @api.marshal_with(IndexApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'Index not found')
    @ns_db.response(500, 'Internal server error')
    def get(self, db_name, index_name):
        """Get an index"""
        abort(HTTPStatus.NOT_IMPLEMENTED)

    @ns_db.doc('delete_index')
    @api.marshal_with(NewIndexApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'Index not found')
    @ns_db.response(500, 'Internal server error')
    def delete(self, db_name, index_name):
        """Delete an index"""
        abort(HTTPStatus.NOT_IMPLEMENTED)
