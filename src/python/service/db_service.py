import pymongo
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from werkzeug.exceptions import Conflict, NotFound, InternalServerError

from api.model.DatabaseModel import DatabaseModel


class DBService(object):
    instance = None

    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kargs)
        return cls.instance

    def __init__(self):
        self.mongo_client = MongoClient('localhost', 27017,
                                        username='root',
                                        password='password')
        self.db_mongo = self.mongo_client['taranis']

        self.databases_collection = self.db_mongo["databases"]
        self.databases_collection.create_index(
            [("name", pymongo.DESCENDING)],
            unique=True
        )

        self.vector_collection = self.db_mongo["vector"]
        self.vector_collection.create_index(
            [("db", pymongo.ASCENDING), ("id", pymongo.ASCENDING)],
            unique=True
        )

    def list_database(self):
        cursor = self.databases_collection.find()
        return [d for d in cursor]

    def create_database(self, database: DatabaseModel):
        try:
            database.created_at = datetime.now()
            database.updated_at = database.created_at
            database.size = 0

            self.databases_collection.insert_one(database.__dict__)
        except DuplicateKeyError as e:
            raise Conflict("Database name {} already exists".format(database.name))
        return database

    def get_database(self, db_name):
        database = self.databases_collection.find_one(dict(name=db_name))
        if database is None:
            raise NotFound("Database {} not found".format(db_name))
        return database

    def delete_database(self, db_name: str):
        res = self.databases_collection.delete_one(dict(name=db_name))
        if res.deleted_count != 1:
            raise NotFound("Database {} not found".format(db_name))

    def put_vectors(self, db_name, vectors, index=None):
        for v in vectors:
            v["db"] = db_name
        res = self.vector_collection.insert_many(vectors)
        if res.acknowledged is not True:
            raise InternalServerError("Can't add these vectors in database")
