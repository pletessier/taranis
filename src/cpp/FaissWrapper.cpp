//
// Created by pletessier on 05/05/19.
//

#include <iostream>
#include <cstdio>
#include <cstdlib>

#include <memory>
#include <vector>
#include <thread>

#include <faiss/IndexIVF.h>
#include <faiss/IndexFlat.h>
#include <faiss/IndexIVFPQ.h>
#include <faiss/IndexBinaryIVF.h>
#include <faiss/AutoTune.h>
#include <faiss/index_io.h>
#include <faiss/IVFlib.h>
#include <faiss/VectorTransform.h>

#include "FaissWrapper.h"
#include "RedisService.h"


using namespace faiss;


FaissWrapper::FaissWrapper(std::string redis_host, size_t redis_port, std::uint32_t timeout_msecs,
                           std::int32_t max_reconnects, std::uint32_t reconnect_interval_msecs) {

    this->data_service = new RedisService();
    this->data_service->connect(redis_host, redis_port, timeout_msecs, max_reconnects, reconnect_interval_msecs);

}


int FaissWrapper::create_index(std::string db_name, std::string index_name, int dimension, const char *index_type,
                               MetricType metric_type, int n_probes) {
    std::cout << "Creating Index with metric_type " << metric_type << std::endl;
    std::unique_ptr<Index> index = std::unique_ptr<Index>(index_factory(dimension, index_type, metric_type));
    ParameterSpace().set_index_parameter(index.get(), "nprobe", n_probes);
    this->data_service->saveIndex(db_name, index_name, index.get());
    return 1;
}

int FaissWrapper::delete_index(std::string db_name, std::string index_name){
    std::cout << "Delete Index " << index_name << std::endl;
    this->data_service->deleteIndex(db_name, index_name);
    return 1;
}

bool FaissWrapper::get_index(std::string db_name, std::string index_name) {
    Index *index = this->data_service->loadIndex(db_name, index_name);
    return index != NULL;
}

bool FaissWrapper::train_model(std::string db_name, std::string index_name, int count, py::array_t<float> vectors) {

    Index *index = this->data_service->loadIndex(db_name, index_name);
    std::cout << "Start training" << std::endl;
    index->train(count, vectors.data());
    std::cout << "Model is trained" << std::endl;
    this->data_service->saveIndex(db_name, index_name, index);
    return true;
}

bool FaissWrapper::encode_vectors(std::string db_name, std::string index_name, int count, py::array_t<float> vectors, py::array_t<int64_t> ids) {

    Index *index = this->data_service->loadIndex(db_name, index_name);

    IndexIVF *index_ivf = ivflib::extract_index_ivf(index);
    std::vector<Index::idx_t> list_nos(count);
    std::vector<uint8_t> codes(index_ivf->code_size * count);
    index_ivf->quantizer->assign(count, vectors.data(), list_nos.data());
    index_ivf->encode_vectors(count, vectors.data(), list_nos.data(), codes.data());
    this->data_service->addVectors(db_name, index_name, ids.data(), list_nos, codes.data(), index_ivf->code_size);

    return true;
}


