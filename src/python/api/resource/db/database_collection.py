#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask_restplus import Resource
from flask_restplus._http import HTTPStatus

from api.model.DatabaseModel import DatabaseModel, CreationModel, Model
from service.db_service import DBService
from src.python.api.restplus import api, ns_db

logger = logging.getLogger(__name__)


@ns_db.route('/')
class DatabaseCollectionResource(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.db_service = DBService()

    @ns_db.doc('list_db')
    @api.marshal_with(Model, as_list=True, code=HTTPStatus.OK)
    @ns_db.response(500, 'Internal server error')
    def get(self):
        """List all databases"""
        databases = self.db_service.list_database()
        return databases, HTTPStatus.OK

    @ns_db.doc('post_db')
    @api.expect(CreationModel)
    @api.doc(model='CreationModel', body=CreationModel)
    @api.marshal_with(Model, code=HTTPStatus.CREATED)
    @ns_db.response(HTTPStatus.CONFLICT, 'Database name already exists')
    @ns_db.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error')
    def post(self):
        """Create a database"""
        database: DatabaseModel = DatabaseModel(api.payload)
        self.db_service.create_database(database)
        return database, HTTPStatus.CREATED
