// Copyright (C) 2019 Pierre Letessier
// This source code is licensed under the BSD 3 license found in the
// LICENSE file in the root directory of this source tree.

#include "taranis.h"
#include <pybind11/pybind11.h>

#include <iostream>
#include <cstdio>
#include <cstdlib>

#include "FaissWrapper.h"
#include "SearchResult.h"

#include <pybind11/stl.h>

namespace py = pybind11;
using namespace faiss;

typedef Index::idx_t idx_t;


class Faiss {
};


PYBIND11_MODULE(cpp_taranis, m) {
    m.doc() = "documentation string";

    py::class_<Faiss> myclass(m, "Faiss");
    py::enum_<MetricType>(myclass, "MetricType")
            .value("METRIC_INNER_PRODUCT", faiss::METRIC_INNER_PRODUCT)
            .value("METRIC_L2", faiss::METRIC_L2)
            .export_values();

    py::class_<SearchResult>(m, "SearchResult", py::module_local())
            .def_property("knns", &SearchResult::getKnns, &SearchResult::setKnns, py::return_value_policy::take_ownership)
            .def_property("dists", &SearchResult::getDists, &SearchResult::setDists, py::return_value_policy::take_ownership);

    py::class_<Index>(m, "Index", py::module_local());


    py::class_<FaissWrapper>(m, "FaissWrapper", py::module_local())
            .def(py::init<std::string, size_t, std::uint32_t, std::int32_t, std::uint32_t>())
            .def("create_index", &FaissWrapper::create_index)
            .def("delete_index", &FaissWrapper::delete_index)
            .def("clear_index", &FaissWrapper::clear_index)
            .def("get_index", &FaissWrapper::get_index)
            .def("train_model", &FaissWrapper::train_model)
            .def("encode_vectors", &FaissWrapper::encode_vectors)
            .def("search_vectors", &FaissWrapper::search_vectors);
}
