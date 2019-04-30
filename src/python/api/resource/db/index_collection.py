#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask_restplus import Resource, abort
from flask_restplus._http import HTTPStatus

from api.model.IndexModel import IndexModel
from service.taranis_service import TaranisService
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/<string:db_name>/index')
class IndexCollectionResource(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.db_service = TaranisService()

    @ns_db.doc('list_index')
    @api.marshal_with(IndexModel.IndexModel, as_list=True, code=HTTPStatus.OK)
    @ns_db.response(404, 'Index not found')
    @ns_db.response(500, 'Internal server error')
    def get(self, db_name):
        """List all indices"""
        abort(HTTPStatus.NOT_IMPLEMENTED)

    @ns_db.doc('post_index')
    @api.expect(IndexModel.IndexCreationModel)
    @api.marshal_with(IndexModel.IndexModel, code=HTTPStatus.CREATED)
    @ns_db.response(HTTPStatus.CONFLICT, 'Index name already exists')
    @ns_db.response(500, 'Internal server error')
    def post(self, db_name):
        """Create an index"""
        index = IndexModel(api.payload)
        index = self.db_service.create_index(db_name, index)
        return index

