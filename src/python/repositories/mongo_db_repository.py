# Copyright (C) 2019 Pierre Letessier
# This source code is licensed under the BSD 3 license found in the
# LICENSE file in the root directory of this source tree.
"""
MongoDB Repository
"""
import numpy as np
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo.results import DeleteResult

from errors.taranis_error import TaranisAlreadyExistsError
from repositories.db_repository import AbstractDatabaseRepository


class MongoDBDatabaseRepository(AbstractDatabaseRepository):

    def __init__(self, host='localhost', port=27017, username='root', password='password'):
        self.mongo_client = MongoClient(host, port,
                                        username=username,
                                        password=password)
        self.db_mongo = self.mongo_client['taranis']

        self.databases_collection = self.db_mongo["databases"]
        self.databases_collection.create_index(
            [("name", pymongo.DESCENDING)],
            unique=True
        )

        self.vector_collection = self.db_mongo["vector"]
        self.vector_collection.create_index(
            [("db_name", pymongo.ASCENDING), ("id", pymongo.ASCENDING)],
            unique=True
        )

        self.indices_collection = self.db_mongo["indices"]
        self.indices_collection.create_index(
            [("index_name", pymongo.DESCENDING), ("db_name", pymongo.DESCENDING)],
            unique=True
        )

    def get_all_databases(self):
        cursor = self.databases_collection.find()
        return [d for d in cursor]

    def create_one_database(self, database):
        try:
            res = self.databases_collection.insert_one(database)
            return res.inserted_id
        except DuplicateKeyError:
            raise TaranisAlreadyExistsError("Database {} already exists".format(database['name']))

    def find_one_database_by_name(self, name):
        return self.databases_collection.find_one(dict(name=name))

    def delete_one_database_by_name(self, name):
        res: DeleteResult = self.databases_collection.delete_one(dict(name=name))
        return res.deleted_count == 1

    def delete_vectors_by_database_name(self, name: str) -> bool:
        res = self.vector_collection.delete_many(dict(db_name=name))
        # TODO DO better
        return True

    def create_vectors(self, vectors: []) -> bool:
        res = self.vector_collection.insert_many(vectors)
        return len(res.inserted_ids) == len(vectors)

    def create_one_index(self, index) -> str:
        res = self.indices_collection.insert_one(index)
        return res.inserted_id

    def delete_one_index(self, index) -> bool:
        res: DeleteResult = self.indices_collection.delete_one(dict(index_name=index.index_name, db_name=index.db_name))
        return res.deleted_count == 1

    def find_one_index_by_index_name_and_db_name(self, index_name: str, db_name: str) -> object:
        return self.indices_collection.find_one(dict(index_name=index_name, db_name=db_name))

    def find_vectors_by_database_name(self, name: str, limit=100000, skip=0) -> (np.ndarray, int):
        cursor = self.vector_collection.find(dict(db_name=name)).skip(skip).limit(limit)
        dimension = 128
        count = cursor.count(with_limit_and_skip=True)

        vectors = np.empty((count, dimension), dtype=np.float32)
        ids = np.empty(count, dtype=np.int64)
        i = 0
        for v in cursor:
            vectors[i, :] = np.frombuffer(v["data"], dtype=np.float32)
            ids[i] = v["id"]
            i += 1
        return vectors, count, ids

    def get_vectors(self, db_name: str, ids: [], limit=100000, skip=0) -> list:
        vectors = [None] * len(ids)

        reverse_list = dict()
        for idx, idv in enumerate(ids):
            reverse_list[idv] = idx

        cursor = self.vector_collection.find(dict(db_name=db_name, id={"$in": ids})).skip(skip).limit(limit)
        for v in cursor:
            vectors[reverse_list[v['id']]] = v
        return vectors
