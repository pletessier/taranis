//
// Created by pletessier on 22/04/19.
//

#include "taranis.h"
#include <pybind11/pybind11.h>

#include <iostream>
#include <cstdio>
#include <cstdlib>

#include "FaissWrapper.h"

namespace py = pybind11;
using namespace faiss;

typedef Index::idx_t idx_t;


//int add(int i, int j) {
//    return i + j;
//}




class Faiss{};


PYBIND11_MODULE(cpp_taranis, m) {
    m.doc() = "documentation string";

//    m.def("add", &add);
//    m.def("create_index", &create_index);

    py::class_<Faiss> myclass(m, "Faiss");
    py::enum_<MetricType>(myclass, "MetricType")
            .value("METRIC_INNER_PRODUCT", faiss::METRIC_INNER_PRODUCT)
            .value("METRIC_L2", faiss::METRIC_L2)
            .export_values();

//    py::class_<Faiss> redisService(m, "RedisService");

    py::class_<FaissWrapper> (m, "FaissWrapper", py::module_local())
            .def(py::init<std::string, size_t, std::uint32_t, std::int32_t, std::uint32_t>())
            .def("create_index", &FaissWrapper::create_index)
            .def("delete_index", &FaissWrapper::delete_index)
            .def("get_index", &FaissWrapper::get_index)
            .def("train_model", &FaissWrapper::train_model)
            .def("encode_vectors", &FaissWrapper::encode_vectors);
}
