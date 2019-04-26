#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask_restplus import Resource, abort
from flask_restplus._http import HTTPStatus

from api.model.VectorApiModel import VectorApiModel
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/<string:db_name>/vector')
class VectorResource(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    @ns_db.doc('get_vectors')
    @api.marshal_with(VectorApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'Vector not found')
    @ns_db.response(500, 'Internal server error')
    @ns_db.param(name="index", description="Name of the index")
    def get(self, db_name):
        '''
        Get a list of vectors
        '''
        vector = None
        if vector is None:
            abort(404, 'Vector not found')
        return vector

    @ns_db.doc('put_vectors')
    @api.marshal_with(VectorApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'Vector not found')
    @ns_db.response(500, 'Internal server error')
    @ns_db.param(name="index", description="Name of the index")
    def put(self, db_name):
        '''
        Create a list of vector
        '''
        vector = None
        if vector is None:
            abort(404, 'Vector not found')
        return vector

    @ns_db.doc('patch_vectors')
    @api.marshal_with(VectorApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'Vector not found')
    @ns_db.response(500, 'Internal server error')
    @ns_db.param(name="index", description="Name of the index")
    def patch(self, db_name):
        '''
        Update a list of vector metadata
        '''
        vector = None
        if vector is None:
            abort(404, 'Vector not found')
        return vector

    @ns_db.doc('delete_vectors')
    @api.marshal_with(VectorApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'Vector not found')
    @ns_db.response(500, 'Internal server error')
    @ns_db.param(name="index", description="Name of the index")
    def delete(self, db_name):
        '''
        Delete a list of vector
        '''
        vector = None
        if vector is None:
            abort(404, 'Vector not found')
        return vector
