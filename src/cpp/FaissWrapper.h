//
// Created by pletessier on 05/05/19.
//

#ifndef CPP_TARANIS_FAISSWRAPPER_H
#define CPP_TARANIS_FAISSWRAPPER_H

#include <faiss/IndexIVF.h>
#include <faiss/IndexFlat.h>
#include <faiss/IndexIVFPQ.h>
#include <faiss/IndexBinaryIVF.h>
#include <faiss/AutoTune.h>
#include <faiss/index_io.h>
#include <faiss/IVFlib.h>
#include <faiss/VectorTransform.h>
#include "RedisService.h"
#include "SearchResult.h"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>


namespace py = pybind11;

class FaissWrapper {

public:
    FaissWrapper(std::string redis_host, size_t redis_port, std::uint32_t timeout_msecs, std::int32_t max_reconnects,
                 std::uint32_t reconnect_interval_msecs);

    int create_index(std::string db_name, std::string index_name, int dimension, const char *index_type,
                     faiss::MetricType metric_type, int n_probes);

    int delete_index(std::string db_name, std::string index_name);

    bool get_index(std::string db_name, std::string index_name);

    bool train_model(std::string db_name, std::string index_name, int count, py::array_t<float> vectors);

    bool encode_vectors(std::string db_name, std::string index_name, int count, py::array_t<float> vectors, py::array_t<int64_t> ids);

    int search_vectors(std::string db_name, std::string index_name, py::array_t<float> raw_queries, int k, int n_probe);

private:
    RedisService *data_service;

};


#endif //CPP_TARANIS_FAISSWRAPPER_H
