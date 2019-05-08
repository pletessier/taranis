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


FaissWrapper::FaissWrapper(std::string redis_host, size_t redis_port, std::uint32_t timeout_msecs, std::int32_t max_reconnects, std::uint32_t reconnect_interval_msecs){

    this->redis = new RedisService();
    this->redis->connect(redis_host, redis_port, timeout_msecs, max_reconnects, reconnect_interval_msecs);

}


int FaissWrapper::create_index(std::string db_name, std::string index_name, int dimension, const char *index_type, MetricType metric_type, int n_probes){
    std::cout << "Creating Index with metric_type " << metric_type << std::endl;

    std::unique_ptr<Index> index = std::unique_ptr<Index>(index_factory(dimension, index_type, metric_type));
    ParameterSpace().set_index_parameter(index.get(), "nprobe", n_probes);

//    write_index(index.get(), "toto.index");

    this->redis->saveIndex(db_name, index_name, index.get());

    return 1;
}

bool FaissWrapper::get_index(std::string db_name, std::string index_name){

    Index* index = this->redis->loadIndex(db_name, index_name);
    return index != NULL;
}

bool FaissWrapper::train_model(std::string db_name, std::string index_name, int count, py::array_t<float> vectors){

    Index* index = this->redis->loadIndex(db_name, index_name);

//    std::cout << "vectors.size() = " << vectors.size() << std::endl;

    std::cout << "Start training" << std::endl;
    index->train(count, vectors.data());
    std::cout << "Model is trained" << std::endl;
    return true;

}