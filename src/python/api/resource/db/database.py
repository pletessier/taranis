#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from flask_restplus import Resource, abort
from flask_restplus._http import HTTPStatus

from api.model.DatabaseApiModel import DatabaseApiModel
from api.model.IndexApiModel import NewIndexApiModel
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/<string:db_name>')
class DatabaseResource(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    @ns_db.doc('get_db')
    @api.marshal_with(DatabaseApiModel, code=HTTPStatus.OK)
    @ns_db.response(HTTPStatus.NOT_FOUND, 'Database not found')
    @ns_db.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def get(self, db_name):
        '''
        Get a database
        '''
        database = None
        if database is None:
            abort(HTTPStatus.NOT_FOUND, 'Database not found')
        return database

    @ns_db.doc('delete_db')
    @api.marshal_with(NewIndexApiModel, code=HTTPStatus.OK)
    @ns_db.response(HTTPStatus.NOT_FOUND, 'Database not found')
    @ns_db.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def delete(self, db_name):
        '''
        Delete a database
        '''
        index = None
        return index
