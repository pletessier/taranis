from pprint import pprint

import numpy as np
import swagger_client
from swagger_client import ApiClient, Configuration, VectorModel, VectorListModel, VectorDataListModel, VectorDataModel
from swagger_client.rest import ApiException

d = 128  # dimension

config = Configuration()
config.host = "http://localhost:8000/api"
config.debug = False
client = ApiClient(config)

# create an instance of the API class
api_instance = swagger_client.DbApi(client)
db_name = 'my_database'
index_name = "basic_index"

try:
    # delete a database
    api_response = api_instance.delete_db(db_name)
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->delete_db: %s\n" % e)

try:
    # Create a database
    payload = swagger_client.DatabaseCreationModel(name=db_name)
    api_response = api_instance.post_db(payload)
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->post_db: %s\n" % e)

try:
    # Get a database
    api_response = api_instance.get_db(db_name)
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->get_db: %s\n" % e)

try:
    # Delete an index
    api_response = api_instance.delete_index(db_name, index_name)
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->post_index: %s\n" % e)


try:
    # Create an index
    payload = swagger_client.IndexCreationModel(name=index_name,
                                                config=dict(index_type="IVFPQ",
                                                            dimension=d,
                                                            n_list=32,
                                                            metric="METRIC_L2",
                                                            n_probes=4))
    api_response = api_instance.post_index(db_name, payload)
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->post_index: %s\n" % e)

try:
    # get an index
    api_response = api_instance.get_index(db_name, index_name)
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->get_index: %s\n" % e)

n_batch = 10
n_training_vectors = 10000


try:
    id = 0
    for b in range(0, n_batch):
        payload = VectorListModel()
        vectors = []
        for i in range(b * n_training_vectors, (b + 1) * n_training_vectors):
            data = np.random.random_sample((d,)).tolist()
            metadata = dict(aaa="aaa", bbb="bbb")
            v = VectorModel(id="{}".format(id), data=data, metadata=metadata)
            id += 1
            vectors.append(v)
        payload.vectors = vectors
        api_response = api_instance.put_vectors(db_name, payload, index_name=index_name)
        pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->put_vectors: %s\n" % e)

try:
    # train an index
    api_response = api_instance.post_index_model(db_name, index_name)
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->post_index_model: %s\n" % e)

try:
    # reencode all vectors in database
    api_response = api_instance.post_reindex(db_name, index_name)
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->post_reindex: %s\n" % e)

try:

    queries = VectorDataListModel(vectors=list())

    try:
        ids = np.random.randint(0, 100000, 10, np.int64).tolist()
        param_id = '|'.join(str(i) for i in ids)
        api_response = api_instance.get_vectors(db_name, ids=param_id)

        for v in api_response.vectors:
            data = v.data
            queries.vectors.append(
                VectorDataModel(data=data)
            )
    except ApiException as e:
        print("Exception when calling DbApi->get_vectors: %s\n" % e)

    api_response = api_instance.search(db_name, queries, index=index_name, k=100, n_probe=4)
    # pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->post_reindex: %s\n" % e)
