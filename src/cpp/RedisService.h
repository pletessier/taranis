//
// Created by pletessier on 05/05/19.
//

#ifndef CPP_TARANIS_REDISSERVICE_H
#define CPP_TARANIS_REDISSERVICE_H


#include <string>
#include <faiss/IndexIVF.h>
#include <faiss/IndexFlat.h>
#include <faiss/IndexIVFPQ.h>
#include <faiss/IndexBinaryIVF.h>
#include <faiss/AutoTune.h>
#include <faiss/index_io.h>
#include <faiss/IVFlib.h>
#include <faiss/VectorTransform.h>
#include "RedisIndexIOWriter.h"

using namespace faiss;

class RedisService {

public:
    RedisService();

    bool connect(std::string redis_host, size_t redis_port, std::uint32_t timeout_msecs, std::int32_t max_reconnects,
                 std::uint32_t reconnect_interval_msecs);

    bool saveIndex(std::string db_name, std::string index_name, Index *index);

    Index *loadIndex(std::string db_name, std::string index_name);

    void addVectors(std::string db_name, std::string index_name, const int64_t* ids,
                    std::vector<faiss::Index::idx_t> list_ids,
                    uint8_t *encoded_vectors, size_t code_size);

    void appendId(std::string db_name, std::string index_name, faiss::Index::idx_t list_id, int64_t id);

    void appendCode(std::string db_name, std::string index_name, faiss::Index::idx_t list_id, uint8_t *code,
                    size_t code_size);

    void incrListSize(std::string db_name, std::string index_name, faiss::Index::idx_t list_id);

    void deleteIndex(const std::string& db_name, const std::string& index_name);

    int64_t getListSize(std::string db_name, std::string index_name, faiss::Index::idx_t list_id);

    const uint8_t * getCodes(std::string db_name, std::string index_name, size_t list_no);

    const int64_t * getIds(std::string db_name, std::string index_name, size_t list_id);

private:
    cpp_redis::client *cli;
};


#endif //CPP_TARANIS_REDISSERVICE_H
