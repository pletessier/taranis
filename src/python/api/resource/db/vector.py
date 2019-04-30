#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask import request
from flask_restplus import Resource, abort
from flask_restplus._http import HTTPStatus
from werkzeug.datastructures import FileStorage

from api.model.VectorApiModel import VectorModel, VectorListModel
from service.taranis_service import TaranisService
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/<string:db_name>/vector')
class VectorResource(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.db_service = TaranisService()

    @ns_db.doc('get_vectors')
    @api.marshal_with(VectorModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'Vector not found')
    @ns_db.response(500, 'Internal server error')
    @ns_db.param(name="index", description="Name of the index")
    def get(self, db_name):
        """Get a list of vectors"""
        abort(HTTPStatus.NOT_IMPLEMENTED)

    @ns_db.doc('put_vectors')
    @api.expect(VectorListModel)
    @api.doc(model='VectorListModel', body=VectorListModel, as_list=True)
    @ns_db.response(404, 'Vector not found')
    @ns_db.response(500, 'Internal server error')
    @ns_db.param(name="index", description="Name of the index")
    def put(self, db_name):
        """Add a list of vector"""
        index = request.args.get('index')
        vectors = api.payload["vectors"]
        self.db_service.put_vectors(db_name, vectors, index=index)

    @ns_db.doc('patch_vectors')
    @api.marshal_with(VectorModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'Vector not found')
    @ns_db.response(500, 'Internal server error')
    @ns_db.param(name="index", description="Name of the index")
    def patch(self, db_name):
        """Update a list of vector metadata"""
        abort(HTTPStatus.NOT_IMPLEMENTED)

    @ns_db.doc('delete_vectors')
    @api.marshal_with(VectorModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'Vector not found')
    @ns_db.response(500, 'Internal server error')
    @ns_db.param(name="index", description="Name of the index")
    def delete(self, db_name):
        """Delete a list of vector"""
        abort(HTTPStatus.NOT_IMPLEMENTED)
