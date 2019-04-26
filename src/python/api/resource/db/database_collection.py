#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask_restplus import Resource
from flask_restplus._http import HTTPStatus

from api.model.DatabaseApiModel import DatabaseApiModel, NewDatabaseApiModel
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/')
class DatabaseCollectionResource(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    @ns_db.doc('list_db')
    @api.marshal_with(DatabaseApiModel, as_list=True, code=HTTPStatus.OK)
    @ns_db.response(500, 'Internal server error')
    def get(self, db_name):
        '''
        List all databases
        '''
        index = None

        return index

    @ns_db.doc('post_db')
    @api.expect(NewDatabaseApiModel)
    @api.marshal_with(DatabaseApiModel, code=HTTPStatus.CREATED)
    @ns_db.response(HTTPStatus.CONFLICT, 'Database name already exists')
    @ns_db.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def post(self, db_name):
        '''
        Create a database
        '''
        index = api.payload
        return index
