import json
import struct

import numpy as np
import pymongo
from pymongo import MongoClient
from pymongo.results import DeleteResult

from api.model.IndexModel import IndexModel
from api.model.VectorApiModel import VectorListModel
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
        res: DeleteResult = self.databases_collection.delete_one(dict(name=name))
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

    def find_one_index_by_index_name_and_db_name(self, index_name: str, db_name: str) -> object:
        return self.indices_collection.find_one(dict(name=index_name, db_name=db_name))

    def find_vectors_by_database_name(self, name: str, limit=100000, skip=0) -> (np.ndarray, int):
        cursor = self.vector_collection.find(dict(db=name)).skip(skip).limit(limit)
        dimension = 128
        count = cursor.count(with_limit_and_skip=True)

        vectors = np.empty((count, dimension), dtype=np.dtype('Float32'))
        ids = np.empty((count), dtype=np.dtype('int64'))
        i = 0
        for v in cursor:
            vectors[i, :] = np.frombuffer(v["data"], dtype=np.dtype('Float32'))
            ids[i] = v["id"]
            i += 1
        return vectors, count, ids

    def get_vectors(self, db_name: str, ids: [], limit=100000, skip=0) -> list:

        vectors = []

        cursor = self.vector_collection.find(dict(db=db_name, id={"$in": ids})).skip(skip).limit(limit)
        for v in cursor:
            new_data = list(struct.unpack('f' * int(len(v["data"]) / 4), v['data']))
            new_vector = dict(id=v['id'], data=new_data, metadata=v['metadata'])
            vectors.append(new_vector)

        return vectors
