//
// Created by pletessier on 30/04/19.
//

#include <iostream>
#include <fmt/format.h>
#include "RedisIndexIOWriter.h"


RedisIndexIOWriter::RedisIndexIOWriter(cpp_redis::client* redis, std::string db_name, std::string index_name) {
    this->redis = redis;
    key = fmt::format("db/{}/idx/{}/index", db_name, index_name);
    this->redis->set(key, "", [](cpp_redis::reply &reply) {});
}

RedisIndexIOWriter::~RedisIndexIOWriter() {

}

size_t RedisIndexIOWriter::operator()(const void *ptr, size_t size, size_t nitems) {
    std::string data = std::string((const char *) ptr, size*nitems);
    redis->append(key, data, [](cpp_redis::reply &reply) {});

    return nitems;
}

bool RedisIndexIOWriter::close() {
    redis->sync_commit();
    return true;
}

