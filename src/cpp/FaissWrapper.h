// Copyright (C) 2019 Pierre Letessier
// This source code is licensed under the BSD 3 license found in the
// LICENSE file in the root directory of this source tree.

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
    FaissWrapper(const string &redis_host, size_t redis_port, uint32_t timeout_msecs,
                 int32_t max_reconnects, uint32_t reconnect_interval_msecs);

    int create_index(const std::string &db_name, const std::string &index_name,
                     int dimension, const char *index_type,
                     faiss::MetricType metric_type, int n_probes);

    int delete_index(const std::string &db_name, const std::string &index_name);

    int clear_index(const std::string &db_name, const std::string &index_name);

    Index *get_index(const std::string &db_name, const std::string &index_name);

    bool train_model(const std::string &db_name, const std::string &index_name,
                     int count, const py::array_t<float> &vectors);

    bool encode_vectors(const std::string &db_name, const std::string &index_name, std::uint64_t count,
                        const py::array_t<float> &vectors,
                        const py::array_t<int64_t> &ids);

    SearchResult *
    search_vectors(const std::string &db_name, const std::string &index_name, const py::array_t<float> &raw_queries,
                   std::uint32_t k, std::uint32_t n_probe);

private:

    RedisService *data_service;
};


#endif //CPP_TARANIS_FAISSWRAPPER_H
