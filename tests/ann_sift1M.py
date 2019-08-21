from __future__ import print_function

import json
import logging
import sys

import grpc
import numpy as np
# set up logger
from grpc._channel import _Rendezvous
from math import log2

import taranis_pb2
import taranis_pb2_grpc

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # anything debug and above passes through to the handler level
fh = logging.StreamHandler(stream=sys.stdout)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


def ivecs_read(fname):
    a = np.fromfile(fname, dtype='int32')
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy()


def fvecs_read(fname):
    return ivecs_read(fname).view('float32')


def bvecs_read(fname):
    a = np.fromfile(fname, dtype='uint8')
    d = a[:4].view('uint8')[0]
    return a.reshape(-1, d + 4)[:, 4:].copy()


def load_dataset(dir) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
    logger.info("Loading dataset in {}".format(dir))

    xb = None
    xq = None
    xt = None
    gt = None

    try:
        xt = fvecs_read("{}/sift_learn.fvecs".format(dir))
    except FileNotFoundError:
        xt = bvecs_read("{}/sift_learn.bvecs".format(dir))
    xb = fvecs_read("{}/sift_base.fvecs".format(dir))
    xq = fvecs_read("{}/sift_query.fvecs".format(dir))
    gt = ivecs_read("{}/sift_groundtruth.ivecs".format(dir))
    logger.info("done")

    return xb, xq, xt, gt


DB_NAME = 'sift1M'
INDEX_NAME = 'basic_index'
N_PROBES = 4
# DIMENSION = 128  # dimension
# N_LISTS = 4096
# n_batch = 10000
# n_training_vectors = 1000

MAX_VECTORS_PER_BATCH = 7000

HOST = 'ogmios.priv.ina'
# HOST = 'localhost'
PORT = 50051


def run():
    xb, xq, xt, gt = load_dataset("/home/pletessier/Dev/pletessier/taranis/data/{}".format(DB_NAME))

    n_vectors, dimension = xb.shape
    n_lists = 2 ** (int(log2(n_vectors / 2048)) + 1)

    with grpc.insecure_channel('{}:{}'.format(HOST, PORT)) as channel:
        stub = taranis_pb2_grpc.TaranisStub(channel)

        try:
            # Delete the database if it already exists, and recreate it
            try:
                my_database = stub.getDatabase(taranis_pb2.DatabaseNameModel(name=DB_NAME))
                logging.info("Found database {}".format(my_database.name))
                stub.deleteDatabase(taranis_pb2.DatabaseNameModel(name=DB_NAME))
                logging.info("Deleted database {}".format(DB_NAME))
            except _Rendezvous as e:
                logging.info("{} : {}".format(e.code(), e.details()))

            response = stub.createDatabase(taranis_pb2.NewDatabaseModel(name=DB_NAME))
            logging.info("Created database {} at {}".format(response.name, response.created_at))

            # Check if database exists
            my_database = stub.getDatabase(taranis_pb2.DatabaseNameModel(name=DB_NAME))
            logging.info("Found database {}".format(my_database.name))

            # Delete the index if it already exists and recreate it
            try:
                my_index = stub.getIndex(taranis_pb2.IndexQueryModel(db_name=DB_NAME, index_name=INDEX_NAME))
                logging.info("Found Index {}".format(my_index.index_name))
                stub.deleteIndex(taranis_pb2.IndexQueryModel(db_name=DB_NAME, index_name=INDEX_NAME))
                logging.info("Deleted Index {}".format(my_index.index_name))
            except _Rendezvous as e:
                logging.info("{} : {}".format(e.code(), e.details()))

            response = stub.createIndex(taranis_pb2.NewIndexModel(db_name=DB_NAME, index_name=INDEX_NAME,
                                                                  config=json.dumps(dict(index_type="IVFPQ",
                                                                                         dimension=dimension,
                                                                                         n_list=n_lists,
                                                                                         metric="METRIC_L2",
                                                                                         n_probes=N_PROBES))))
            logging.info("Created index {} at {}".format(response.index_name, response.created_at))

            my_index = stub.getIndex(taranis_pb2.IndexQueryModel(db_name=DB_NAME, index_name=INDEX_NAME))
            logging.info("Found Index {}".format(my_index.index_name))

            i = 0
            vid = 0
            while i < n_vectors:
                c = min(i + MAX_VECTORS_PER_BATCH, n_vectors) - i
                logging.info("Adding {} vectors : {}%".format(c, (i * 1.0 / n_vectors) * 100))
                i = i + c
                payload = taranis_pb2.NewVectorsModel()
                payload.db_name = DB_NAME
                for j in range(0, c):
                    v = payload.vectors.add()
                    v.id = vid
                    v.data = xb[vid].tobytes()
                    v.metadata = json.dumps(dict(aaa="aaa", bbb="bbb"))
                    vid += 1
                response = stub.addVectors(payload)

            # Train the index
            # TODO Train the index from provided vectors in dataset
            logging.info("Training index {} for db {}".format(INDEX_NAME, DB_NAME))
            response = stub.trainIndex(taranis_pb2.IndexQueryModel(db_name=DB_NAME, index_name=INDEX_NAME))
            logging.info("Trained index {} for db {}".format(INDEX_NAME, DB_NAME))

            # reencode all vectors in database
            logging.info("Encoding all vectors in index {} for db {}".format(INDEX_NAME, DB_NAME))
            response = stub.reindex(taranis_pb2.IndexQueryModel(db_name=DB_NAME, index_name=INDEX_NAME))
            logging.info("Encoded all vectors in index {} for db {}".format(INDEX_NAME, DB_NAME))

            qid = 0
            n_query_per_batch = 100
            recalls_at = {1: 0.0, 4: 0.0, 16: 0.0, 64: 0.0, 128: 0.0}
            n_queries = xq.shape[0]
            for i in range(0, n_queries, n_query_per_batch):
                qid = i
                query = taranis_pb2.VectorsQueryModel(db_name=DB_NAME)
                search_request = taranis_pb2.SearchRequestModel(db_name=DB_NAME, index_name=INDEX_NAME,
                                                                k=128, n_probe=N_PROBES)

                for v in range(0, n_query_per_batch):
                    search_request.vectors.append(xq[qid].tobytes())
                    qid = qid + 1

                result_list: taranis_pb2.SearchResultListModel = stub.searchVectors(search_request)

                qid = i
                for sr in result_list.results:
                    for r, v in recalls_at.items():
                        if gt[qid][0] in sr.knn[0:r]:
                            recalls_at[r] = v + 1
                    qid = qid + 1
                logging.info("Searching: {:.0f}%".format((i * 1.0 / n_queries) * 100))

            logging.info("Results")
            for r, v in recalls_at.items():
                v = v * 1.0 / n_queries
                logging.info("Recall @ {} = {:.6f}".format(r, v))

            # Test add more vectors

            count_vectors_per_batch = 1000
            n_batch = 1000
            vid = 1000000
            for i in range(0, n_batch):
                # logging.info("Adding {} vectors : {}%".format(c, (i * 1.0 / n_vectors) * 100))
                # i = i + c
                payload = taranis_pb2.NewVectorsModel()
                payload.db_name = DB_NAME
                payload.db_name = INDEX_NAME

                new_vectors = np.random.random_sample((dimension, count_vectors_per_batch))

                for j in range(0, count_vectors_per_batch):
                    v = payload.vectors.add()
                    v.id = vid
                    v.data = new_vectors[:,j].tobytes()
                    v.metadata = json.dumps(dict(aaa="aaa", bbb="bbb"))
                    vid += 1
                response = stub.addVectors(payload)

            qid = 0
            n_query_per_batch = 100
            recalls_at = {1: 0.0, 4: 0.0, 16: 0.0, 64: 0.0, 128: 0.0}
            n_queries = xq.shape[0]
            for i in range(0, n_queries, n_query_per_batch):
                qid = i
                query = taranis_pb2.VectorsQueryModel(db_name=DB_NAME)
                search_request = taranis_pb2.SearchRequestModel(db_name=DB_NAME, index_name=INDEX_NAME,
                                                                k=128, n_probe=N_PROBES)

                for v in range(0, n_query_per_batch):
                    search_request.vectors.append(xq[qid].tobytes())
                    qid = qid + 1

                result_list: taranis_pb2.SearchResultListModel = stub.searchVectors(search_request)

                qid = i
                for sr in result_list.results:
                    for r, v in recalls_at.items():
                        if gt[qid][0] in sr.knn[0:r]:
                            recalls_at[r] = v + 1
                    qid = qid + 1
                logging.info("Searching: {:.0f}%".format((i * 1.0 / n_queries) * 100))

            logging.info("Results")
            for r, v in recalls_at.items():
                v = v * 1.0 / n_queries
                logging.info("Recall @ {} = {:.6f}".format(r, v))

        except _Rendezvous as e:
            logging.error("{} : {}".format(e.code(), e.details()))


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    run()
