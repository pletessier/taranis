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

int FaissWrapper::delete_index(std::string db_name, std::string index_name) {
    std::cout << "Delete Index " << index_name << std::endl;
    this->data_service->deleteIndex(db_name, index_name);
    return 1;
}

int FaissWrapper::clear_index(std::string db_name, std::string index_name) {
    std::cout << "Clear Index " << index_name << std::endl;
    this->data_service->clearIndex(db_name, index_name);
    return 1;
}

Index* FaissWrapper::get_index(std::string db_name, std::string index_name) {
    Index *index = this->data_service->loadIndex(db_name, index_name);
    return index;
}

bool FaissWrapper::train_model(std::string db_name, std::string index_name, int count, py::array_t<float> vectors) {

    Index *index = this->data_service->loadIndex(db_name, index_name);
    std::cout << "Start training" << std::endl;
    index->train(count, vectors.data());
    std::cout << "Model is trained" << std::endl;
    this->data_service->saveIndex(db_name, index_name, index);
    return true;
}

bool FaissWrapper::encode_vectors(std::string db_name, std::string index_name, int count, py::array_t<float> vectors,
                                  py::array_t<int64_t> ids) {

    Index *index = this->data_service->loadIndex(db_name, index_name);

    IndexIVF *index_ivf = ivflib::extract_index_ivf(index);
    std::vector<Index::idx_t> list_nos(count);
    std::vector<uint8_t> codes(index_ivf->code_size * count);
    index_ivf->quantizer->assign(count, vectors.data(), list_nos.data());
    index_ivf->encode_vectors(count, vectors.data(), list_nos.data(), codes.data());
    this->data_service->addVectors(db_name, index_name, ids.data(), list_nos, codes.data(), index_ivf->code_size);

    return true;
}


SearchResult*
FaissWrapper::search_vectors(std::string db_name, std::string index_name, py::array_t<float> raw_queries, int k,
                             int n_probe) {

    size_t nq = raw_queries.shape(0);
    size_t dimension = raw_queries.shape(1);

    std::cout << "Search " << k << " NN in " << db_name << ":" << index_name << " with " << nq
              << " vectors of dimension " << dimension << " and " << n_probe << " probes" << std::endl;

//    const float *xqt = xq.data();
    const float *xqt = raw_queries.data();

    Index *index = this->data_service->loadIndex(db_name, index_name);

    IndexIVF *index_ivf = ivflib::extract_index_ivf(index);
    // quantize the queries to get the inverted list ids to visit.

    std::vector<Index::idx_t> q_lists(nq * n_probe);
    std::vector<float> q_dis(nq * n_probe);

    index_ivf->quantizer->search(nq, xqt, n_probe, q_dis.data(), q_lists.data());

    // object that does the scanning and distance computations.
//    std::unique_ptr<InvertedListScanner> scanner(index_ivf->get_InvertedListScanner());
    InvertedListScanner* scanner = index_ivf->get_InvertedListScanner();

    float default_dis = index->metric_type == METRIC_L2 ? HUGE_VAL : -HUGE_VAL;
    int dt = index->d;

//    auto sr = std::unique_ptr<SearchResult>(new SearchResult());
    SearchResult* sr = new SearchResult();

    for (int i = 0; i < nq; i++) {
        std::vector<Index::idx_t> *I = new std::vector<Index::idx_t>(k, -1);
        std::vector<float> *D = new std::vector<float>(k, default_dis);

        scanner->set_query(xqt + i * dt);

        for (int j = 0; j < n_probe; j++) {

            auto list_no = static_cast<size_t>(q_lists[i * n_probe + j]);
            if (0 > list_no) continue;
            scanner->set_list(list_no, q_dis[i * n_probe + j]);

            int64_t list_size = this->data_service->getListSize(db_name, index_name, list_no);
            const uint8_t *codes = this->data_service->getCodes(db_name, index_name, list_no, list_size, index_ivf->code_size);
            const int64_t *ids = this->data_service->getIds(db_name, index_name, list_no, list_size);

            scanner->scan_codes(list_size, codes, ids, D->data(), I->data(), k);

            delete[] codes;
            delete[] ids;
        }

        // re-order heap
        if (index->metric_type == METRIC_L2) {
            maxheap_reorder(k, D->data(), I->data());
        } else {
            minheap_reorder(k, D->data(), I->data());
        }

//        std::cout << "Query " << i << ": id=" << i << ", K1=" << I->operator[](0) << std::endl;

        sr->getKnns()->push_back(I);
        sr->getDists()->push_back(D);
    }

    delete index;


//    std::cout << "will return" << std::endl;

//    std::cout << "There are  " << sr->getKnns()->size() << " results" << std::endl;

    return sr;
}