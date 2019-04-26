#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask_restplus import Resource, abort
from flask_restplus._http import HTTPStatus

from api.model.IndexTrainingsetApiModel import IndexTrainingSetApiModel
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/<string:db_name>/index/<string:index_name>/trainingset')
class IndexTrainingSetResource(Resource):

    @ns_db.doc('get_index_trainingset')
    @api.marshal_with(IndexTrainingSetApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'IndexTrainingSet not found')
    @ns_db.response(500, 'Internal server error')
    def get(self, db_name):
        '''
        Get the index trainingset
        '''
        trainingset = None
        if trainingset is None:
            abort(404, 'trainingset not found')
        return trainingset

    @ns_db.doc('delete_index_trainingset')
    @api.marshal_with(IndexTrainingSetApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'IndexTrainingSet not found')
    @ns_db.response(500, 'Internal server error')
    def delete(self, db_name):
        '''
        Delete an index trainingset
        '''
        trainingset = None
        return trainingset

    @ns_db.doc('post_index_model')
    @ns_db.expect(IndexTrainingSetApiModel)
    @api.marshal_with(IndexTrainingSetApiModel, code=HTTPStatus.OK)
    @ns_db.response(404, 'IndexTrainingSet not found')
    @ns_db.response(500, 'Internal server error')
    def post(self, db_name):
        '''
        Add vectors to training set
        '''
        trainingset = None
        return trainingset
