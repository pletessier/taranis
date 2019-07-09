// Copyright (C) 2019 Pierre Letessier
// This source code is licensed under the BSD 3 license found in the
// LICENSE file in the root directory of this source tree.

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

    bool connect(const std::string& redis_host, size_t redis_port, std::uint32_t timeout_msecs, std::int32_t max_reconnects,
                 std::uint32_t reconnect_interval_msecs);

    bool saveIndex(const std::string& db_name, const std::string& index_name, Index *index);

    Index *loadIndex(const std::string& db_name, const std::string& index_name);

    void addVectors(const std::string& db_name, const std::string& index_name, const int64_t* ids,
                    std::vector<faiss::Index::idx_t> list_ids,
                    uint8_t *encoded_vectors, size_t code_size);

    void appendId(const std::string& db_name, const std::string& index_name, faiss::Index::idx_t list_id, int64_t id);

    void appendCode(const std::string& db_name, const std::string& index_name, faiss::Index::idx_t list_id, uint8_t *code,
                    size_t code_size);

    void incrListSize(const std::string& db_name, const std::string& index_name, faiss::Index::idx_t list_id);

    void deleteInvertedLists(const std::string &db_name, const std::string &index_name);

    void deleteIndex(const std::string& db_name, const std::string& index_name);

    int64_t getListSize(const std::string& db_name, const std::string& index_name, faiss::Index::idx_t list_id);

    const uint8_t * getCodes(const std::string& db_name, const std::string& index_name, size_t list_no, int64_t list_size, int code_size);

    const int64_t * getIds(const std::string& db_name, const std::string& index_name, size_t list_id, int64_t list_size);

    void clearIndex(const std::string& dbName, const std::string& indexName);

private:
    cpp_redis::client *cli{};



    void deleteFromPattern(const std::string &pattern);
};


#endif //CPP_TARANIS_REDISSERVICE_H
