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
    def get(self, db_name):
        '''
        Get an index
        '''
        index = None
        if index is None:
            abort(404, 'Index not found')
        return index

    @ns_db.doc('delete_index')
    @api.marshal_with(NewIndexApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'Index not found')
    @ns_db.response(500, 'Internal server error')
    def delete(self, db_name):
        '''
        Delete an index
        '''
        index = None
        return index

#
# @ns.route('/<string:name>/trainingset')
# class TrainingSetResource(Resource):
#
#     def __init__(self, api=None, *args, **kwargs):
#         super().__init__(api, *args, **kwargs)
#
#     @ns.doc('get_trainingset')
#     @api.marshal_with(IndexApiModel, code=HTTPStatus.OK)
#     @ns.response(404, 'Index not found')
#     @ns.response(500, 'Internal server error')
#     def get(self, name):
#         '''
#         return specific trainingset
#         '''
#         index = None
#         if index is None:
#             abort(404, 'Index not found')
#         return index
