//
// Created by pletessier on 30/04/19.
//

#ifndef CPP_TARANIS_REDISINDEXIOWRITER_H
#define CPP_TARANIS_REDISINDEXIOWRITER_H

#include <faiss/AuxIndexStructures.h>
#include <cpp_redis/core/client.hpp>

using namespace faiss;

class RedisIndexIOWriter : public IOWriter {

public:
    RedisIndexIOWriter(cpp_redis::client* redis, std::string db_name, std::string index_name);

    ~RedisIndexIOWriter();

    size_t operator()(const void *ptr, size_t size, size_t nitems) override;

    bool close();

private:
    cpp_redis::client* redis;
    std::string key;
};


#endif //CPP_TARANIS_REDISINDEXIOWRITER_H
