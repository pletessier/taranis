from __future__ import print_function

import json
import logging
import sys
import time

from utils.chronograph import Chronograph
import grpc
import numpy as np
from grpc._channel import _Rendezvous

import taranis_pb2
import taranis_pb2_grpc


DB_NAME = 'db3'
INDEX_NAME = 'basic_index'
DIMENSION = 128  # dimension
N_LISTS = 4096
n_batch = 10000
n_training_vectors = 1000


# DB_NAME = 'db2'
# INDEX_NAME = 'basic_index'
# DIMENSION = 128  # dimension
# N_LISTS = 4
# n_batch = 100
# n_training_vectors = 1000


# set up logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # anything debug and above passes through to the handler level
fh = logging.StreamHandler(stream=sys.stdout)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = taranis_pb2_grpc.TaranisStub(channel)



        try:

            # # Delete the database if it already exists, and recreate it
            # try:
            #     my_database = stub.getDatabase(taranis_pb2.DatabaseNameModel(name=DB_NAME))
            #     logging.info("Found database {}".format(my_database.name))
            #     stub.deleteDatabase(taranis_pb2.DatabaseNameModel(name=DB_NAME))
            #     logging.info("Deleted database {}".format(DB_NAME))
            # except _Rendezvous as e:
            #     logging.info("{} : {}".format(e.code(), e.details()))
            #
            # response = stub.createDatabase(taranis_pb2.NewDatabaseModel(name=DB_NAME))
            # logging.info("Created database {} at {}".format(response.name, response.created_at))
            #
            # # Check if database exists
            # my_database = stub.getDatabase(taranis_pb2.DatabaseNameModel(name=DB_NAME))
            # logging.info("Found database {}".format(my_database.name))
            #
            # # Delete the index if it already exists and recreate it
            # try:
            #     my_index = stub.getIndex(taranis_pb2.IndexQueryModel(db_name=DB_NAME, index_name=INDEX_NAME))
            #     logging.info("Found Index {}".format(my_index.index_name))
            #     stub.deleteIndex(taranis_pb2.IndexQueryModel(db_name=DB_NAME, index_name=INDEX_NAME))
            #     logging.info("Deleted Index {}".format(my_index.index_name))
            # except _Rendezvous as e:
            #     logging.info("{} : {}".format(e.code(), e.details()))
            #
            # response = stub.createIndex(taranis_pb2.NewIndexModel(db_name=DB_NAME, index_name=INDEX_NAME,
            #                                                       config=json.dumps(dict(index_type="IVFPQ",
            #                                                                              dimension=DIMENSION,
            #                                                                              n_list=N_LISTS,
            #                                                                              metric="METRIC_L2",
            #                                                                              n_probes=4))))
            # logging.info("Created index {} at {}".format(response.index_name, response.created_at))
            #
            # my_index = stub.getIndex(taranis_pb2.IndexQueryModel(db_name=DB_NAME, index_name=INDEX_NAME))
            # logging.info("Found Index {}".format(my_index.index_name))
            #
            # vid = 0
            # for b in range(0, n_batch):
            #     logging.info("Batch {} on {}".format(b, n_batch))
            #     payload = taranis_pb2.NewVectorsModel()
            #     payload.db_name = DB_NAME
            #     for i in range(b * n_training_vectors, (b + 1) * n_training_vectors):
            #         v = payload.vectors.add()
            #         v.id = vid
            #         v.data = np.random.Generator().random((DIMENSION,), dtype=np.float32).tobytes()
            #         # v.data = np.random.random_sample((DIMENSION,)).tobytes()
            #         v.metadata = json.dumps(dict(aaa="aaa", bbb="bbb"))
            #         vid += 1
            #     response = stub.addVectors(payload)
            #     logging.info("Added {} vectors".format(n_training_vectors))
            #
            # # Train the index
            # response = stub.trainIndex(taranis_pb2.IndexQueryModel(db_name=DB_NAME, index_name=INDEX_NAME))
            # logging.info("Trained index {} for db {}".format(INDEX_NAME, DB_NAME))
            #
            # # reencode all vectors in database
            # response = stub.reindex(taranis_pb2.IndexQueryModel(db_name=DB_NAME, index_name=INDEX_NAME))

            cg = Chronograph(name="Testing Chronograph", verbosity=1, logger=logger, log_lvl="INFO", start_timing=False)

            for b in range(0, 100):
                query = taranis_pb2.VectorsQueryModel(db_name=DB_NAME)
                for i in np.random.randint(0, n_batch * n_training_vectors, 100, np.int64).tolist():
                    query.ids.append(i)

                random_vectors: taranis_pb2.VectorsReplyModel = stub.getVectors(query)

                search_request = taranis_pb2.SearchRequestModel(db_name=DB_NAME, index_name=INDEX_NAME, k=100, n_probe=5)
                for v in random_vectors.vectors:
                    search_request.vectors.append(v.data)

                cg.start("searchVectors")
                result_list: taranis_pb2.SearchResultListModel = stub.searchVectors(search_request)
                cg.stop()

                for sr, qid in zip(result_list.results, query.ids):
                    print("{} : {}".format(qid, sr.knn[0]))

            cg.report(printout=True)

        except _Rendezvous as e:
            logging.error("{} : {}".format(e.code(), e.details()))


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    run()
