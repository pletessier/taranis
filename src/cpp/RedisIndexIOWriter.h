// Copyright (C) 2019 Pierre Letessier
// This source code is licensed under the BSD 3 license found in the
// LICENSE file in the root directory of this source tree.

#ifndef CPP_TARANIS_REDISINDEXIOWRITER_H
#define CPP_TARANIS_REDISINDEXIOWRITER_H

#include <faiss/AuxIndexStructures.h>
#include <cpp_redis/core/client.hpp>

using namespace faiss;

class RedisIndexIOWriter : public IOWriter {

public:
    RedisIndexIOWriter(cpp_redis::client* redis, const std::string &db_name, const std::string& index_name);

    ~RedisIndexIOWriter() override;

    size_t operator()(const void *ptr, size_t size, size_t nitems) override;

    bool close();

private:
    cpp_redis::client* redis;
    std::string key;
};


#endif //CPP_TARANIS_REDISINDEXIOWRITER_H
