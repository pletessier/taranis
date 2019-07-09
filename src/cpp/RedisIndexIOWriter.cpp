// Copyright (C) 2019 Pierre Letessier
// This source code is licensed under the BSD 3 license found in the
// LICENSE file in the root directory of this source tree.

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

