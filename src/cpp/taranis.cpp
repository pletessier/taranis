//
// Created by pletessier on 22/04/19.
//

#include "taranis.h"
#include "RedisIndexIOWriter.h"
#include <pybind11/pybind11.h>

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
//#include "InvertedListManager.h"

#include <fmt/printf.h>
#include <cpp_redis/cpp_redis>

namespace py = pybind11;
using namespace faiss;

typedef Index::idx_t idx_t;


int add(int i, int j) {
    return i + j;
}


//std::unique_ptr<Index> make_trained_index(const char *index_type, MetricType metric_type, int dimension, size_t training_vec_count) {
//
//    auto index = std::unique_ptr<Index>(index_factory(dimension, index_type, metric_type));
////    auto xt = make_data(training_vec_count, dimension);
////    index->train(training_vec_count, xt.data());
//    ParameterSpace().set_index_parameter(index.get(), "nprobe", 4);
//    return index;
//}

void create_index(int dimension, const char *index_type, MetricType metric_type, int n_probes){
    std::cout << "Creating Index with metric_type " << metric_type << std::endl;

    auto index = std::unique_ptr<Index>(index_factory(dimension, index_type, metric_type));
    ParameterSpace().set_index_parameter(index.get(), "nprobe", n_probes);


    RedisIndexIOWriter* writer = new RedisIndexIOWriter();

    write_index(index.get(), writer);
}

class Faiss{};


PYBIND11_MODULE(cpp_taranis, m) {
    m.doc() = "documentation string";

    m.def("add", &add);
    m.def("create_index", &create_index);

    py::class_<Faiss> myclass(m, "Faiss");
//
    py::enum_<MetricType>(myclass, "MetricType")
            .value("METRIC_INNER_PRODUCT", faiss::METRIC_INNER_PRODUCT)
            .value("METRIC_L2", faiss::METRIC_L2)
            .export_values();
}
