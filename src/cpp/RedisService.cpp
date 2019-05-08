//
// Created by pletessier on 05/05/19.
//

#include <cpp_redis/core/client.hpp>
#include "RedisService.h"
#include "RedisIndexIOWriter.h"

#include <faiss/IndexIVF.h>
#include <faiss/IndexFlat.h>
#include <faiss/IndexIVFPQ.h>
#include <faiss/IndexBinaryIVF.h>
#include <faiss/AutoTune.h>
#include <faiss/index_io.h>
#include <faiss/IVFlib.h>
#include <faiss/VectorTransform.h>
#include <fmt/format.h>

#include "FaissWrapper.h"
#include "RedisIndexIOWriter.h"

using namespace faiss;


RedisService::RedisService() {}


bool RedisService::connect(std::string redis_host, size_t redis_port,
                           std::uint32_t timeout_msecs,
                           std::int32_t max_reconnects,
                           std::uint32_t reconnect_interval_msecs) {

    const cpp_redis::client::connect_callback_t &connect_callback = nullptr;
    cli = new cpp_redis::client();

    cli->connect(redis_host, redis_port, connect_callback, timeout_msecs, max_reconnects, reconnect_interval_msecs);

    return cli->is_connected();
}

bool RedisService::saveIndex(std::string db_name, std::string index_name, Index* index) {

    auto writer = new RedisIndexIOWriter(cli, db_name, index_name);
    write_index(index, writer);
    writer->close();
    return true;
}

Index* RedisService::loadIndex(std::string db_name, std::string index_name) {

    std::string key = fmt::format("db/{}/idx/{}/index", db_name, index_name);
    std::future<cpp_redis::reply> reply = this->cli->get(key);

    this->cli->sync_commit();

    std::string string_reply = reply.get().as_string();
    const std::vector<uint8_t> data(string_reply.begin(), string_reply.end());

    auto reader = new VectorIOReader();
    reader->data = data;

    Index* index = read_index(reader);
    index->display();

    return index;
}
