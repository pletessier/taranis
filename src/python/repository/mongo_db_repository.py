import json

import pymongo
from pymongo import MongoClient
from pymongo.results import DeleteResult

from api.model.IndexModel import IndexModel
from repository.db_repository import AbstractDatabaseRepository


class MongoDBDatabaseRepository(AbstractDatabaseRepository):

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

        self.indices_collection = self.db_mongo["indices"]
        self.indices_collection.create_index(
            [("name", pymongo.DESCENDING)],
            unique=True
        )

    def get_all_databases(self):
        cursor = self.databases_collection.find()
        return [d for d in cursor]

    def create_one_database(self, database):
        res = self.databases_collection.insert_one(database.__dict__)
        return res.inserted_id

    def find_one_database_by_name(self, name):
        return self.databases_collection.find_one(dict(name=name))

    def delete_one_database_by_name(self, name):
        res : DeleteResult = self.databases_collection.delete_one(dict(name=name))
        return res.deleted_count == 1

    def delete_vectors_by_database_name(self, name: str) -> bool:
        res = self.vector_collection.delete_many(dict(db=name))
        # TODO DO better
        return True

    def create_vectors(self, vectors: []) -> bool:
        res = self.vector_collection.insert_many(vectors)
        return len(res.inserted_ids) == len(vectors)

    def create_one_index(self, index: IndexModel) -> str:
        d = index.todict()
        res = self.indices_collection.insert_one(d)
        return res.inserted_id

    def delete_one_index(self, index: IndexModel) -> bool:
        res: DeleteResult = self.indices_collection.delete_one(dict(name=index.name, db_name=index.db_name))
        return res.deleted_count == 1









