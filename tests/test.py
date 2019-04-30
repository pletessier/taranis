from pprint import pprint

import numpy as np

import swagger_client
from swagger_client.rest import ApiException
from swagger_client import ApiClient, Configuration, VectorModel, VectorListModel

d = 128  # dimension

config = Configuration()
config.host = "http://localhost:8000/api"
config.debug = True
client = ApiClient(config)

# create an instance of the API class
api_instance = swagger_client.DbApi(client)
db_name = 'my_database'

try:
    # delete a database
    api_response = api_instance.delete_db(db_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->delete_db: %s\n" % e)

try:
    # Create a database
    payload = swagger_client.DatabaseCreationModel(name=db_name)
    api_response = api_instance.post_db(payload)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->post_db: %s\n" % e)

try:
    # Get a database
    api_response = api_instance.get_db(db_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->get_db: %s\n" % e)

try:
    # Delete an index
    api_response = api_instance.delete_index(db_name, "basic_index")
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->post_index: %s\n" % e)

try:
    # Create an index
    payload = swagger_client.IndexCreationModel(name="basic_index", config="my config string")
    api_response = api_instance.post_index(db_name, payload)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DbApi->post_index: %s\n" % e)


# try:
#
#     payload = VectorListModel()
#     vectors = []
#     for i in range(1000, 2000):
#         data = np.random.random_sample((d,)).tolist()
#         metadata = dict(aaa="aaa", bbb="bbb")
#         v = VectorModel(id="{}".format(i), data=data, metadata=metadata)
#         vectors.append(v)
#
#     payload.vectors = vectors
#     api_response = api_instance.put_vectors(db_name, payload, index="basic_index")
#     # pprint(api_response)
# except ApiException as e:
#     print("Exception when calling DbApi->put_vectors: %s\n" % e)
