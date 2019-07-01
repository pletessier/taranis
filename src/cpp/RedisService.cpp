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

bool RedisService::saveIndex(std::string db_name, std::string index_name, Index *index) {
    std::cout << "Saving index" << std::endl;
    auto writer = new RedisIndexIOWriter(cli, db_name, index_name);
    write_index(index, writer);
    writer->close();
    std::cout << "Index is saved" << std::endl;
    return true;
}

Index *RedisService::loadIndex(std::string db_name, std::string index_name) {

    std::cout << "Loading index" << std::endl;
    std::string key = fmt::format("db/{}/idx/{}/index", db_name, index_name);
    std::future<cpp_redis::reply> future_reply = this->cli->get(key);

    this->cli->sync_commit();

    cpp_redis::reply reply = future_reply.get();

    if( ! reply.is_string()){
        return nullptr;
    }

    std::string string_reply = reply.as_string();
    const std::vector<uint8_t> data(string_reply.begin(), string_reply.end());

    auto reader = new VectorIOReader();
    reader->data = data;

    Index *index = read_index(reader);
    index->display();
    std::cout << "Index is loaded" << std::endl;

    delete reader;

    return index;
}


void RedisService::addVectors(std::string db_name, std::string index_name, const int64_t *ids,
                              std::vector<faiss::Index::idx_t> list_ids,
                              uint8_t *encoded_vectors, size_t code_size) {

    for (int i = 0; i < list_ids.size(); i++) {
        faiss::Index::idx_t list_id = list_ids[i];

        this->appendId(db_name, index_name, list_id, ids[i]);
        this->appendCode(db_name, index_name, list_id, encoded_vectors + i * code_size, code_size);
        this->incrListSize(db_name, index_name, list_id);
    }
    this->cli->sync_commit();
}

void RedisService::appendId(std::string db_name, std::string index_name, faiss::Index::idx_t list_id, int64_t id) {

    std::string key = fmt::format("db/{}/idx/{}/il/{}/ids", db_name, index_name, list_id);
    std::string sid = std::string((const char *) &(id), sizeof(int64_t));
    this->cli->append(key, sid, [](cpp_redis::reply &reply) {});
}

void RedisService::appendCode(std::string db_name, std::string index_name, faiss::Index::idx_t list_id, uint8_t *code,
                              size_t code_size) {

    std::string scode = std::string((const char *) code, code_size);
    std::string key = fmt::format("db/{}/idx/{}/il/{}/codes", db_name, index_name, list_id);
    this->cli->append(key, scode, [](cpp_redis::reply &reply) {});
}

void RedisService::incrListSize(std::string db_name, std::string index_name, faiss::Index::idx_t list_id) {
    std::string key = fmt::format("db/{}/idx/{}/il/{}/size", db_name, index_name, list_id);
    this->cli->incr(key);
}

void RedisService::deleteFromPattern(const std::string& pattern) {

    std::future<cpp_redis::reply> reply = this->cli->keys(pattern);
    this->cli->sync_commit();
    std::vector<cpp_redis::reply> replies = reply.get().as_array();

    std::vector<std::string> keys = std::vector<std::string>();
    for (auto & r : replies) {
        const std::string& key = r.as_string();
        std::cout << "Removing key " << key << std::endl;
        keys.push_back(key);
    }
    this->cli->del(keys, [](cpp_redis::reply &reply) {});
    this->cli->sync_commit();
}

void RedisService::deleteInvertedLists(const std::string& db_name, const std::string& index_name) {

    std::string pattern = fmt::format("db/{}/idx/{}/il/*", db_name, index_name);
    deleteFromPattern(pattern);
}

void RedisService::deleteIndex(const std::string& db_name, const std::string& index_name) {

    std::string pattern = fmt::format("db/{}/idx/{}/*", db_name, index_name);
    deleteFromPattern(pattern);
}

void RedisService::clearIndex(string dbName, string indexName) {
    deleteInvertedLists(dbName, indexName);
}

int64_t RedisService::getListSize(std::string db_name, std::string index_name, faiss::Index::idx_t list_id) {

    std::string key = fmt::format("db/{}/idx/{}/il/{}/size", db_name, index_name, list_id);
    std::future<cpp_redis::reply> reply = this->cli->get(key);
    this->cli->sync_commit();
    return stol(reply.get().as_string());
}

const uint8_t * RedisService::getCodes(std::string db_name, std::string index_name, size_t list_id, int64_t list_size, int code_size) {

    std::string key = fmt::format("db/{}/idx/{}/il/{}/codes", db_name, index_name, list_id);
    std::future<cpp_redis::reply> reply = this->cli->get(key);
    this->cli->sync_commit();

//    const uint8_t *codes = reinterpret_cast<const uint8_t *>(reply.get().as_string().c_str());
    uint8_t * codes = new uint8_t[list_size*code_size];
    memcpy (codes, reply.get().as_string().c_str(), list_size * code_size * sizeof (uint8_t)) ;
    return codes;
}

const int64_t * RedisService::getIds(std::string db_name, std::string index_name, size_t list_id, int64_t list_size) {

    std::string key = fmt::format("db/{}/idx/{}/il/{}/ids", db_name, index_name, list_id);
    std::future<cpp_redis::reply> reply = this->cli->get(key);
    this->cli->sync_commit();

//    const int64_t *ids = reinterpret_cast<const int64_t *>(reply.get().as_string().c_str());
    int64_t * ids = new int64_t[list_size];
    memcpy (ids, reply.get().as_string().c_str(), list_size * sizeof (int64_t)) ;

    return ids;
}


