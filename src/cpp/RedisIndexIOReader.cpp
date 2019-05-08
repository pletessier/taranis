//
// Created by pletessier on 05/05/19.
//

#include "RedisIndexIOReader.h"


RedisIndexIOReader::RedisIndexIOReader(cpp_redis::client* redis, std::string db_name, std::string index_name) {
    this->redis = redis;
    key = fmt::format("db/{}/idx/{}/index", db_name, index_name);
    std::future<cpp_redis::reply> reply = this->redis->get(key);
    this->redis->sync_commit();
    data = reinterpret_cast<const uint8_t *>(reply.get().as_string().c_str());

}

RedisIndexIOReader::~RedisIndexIOReader() {

}

size_t RedisIndexIOReader::operator()(void *ptr, size_t size, size_t nitems) {


    return nitems;
}

bool RedisIndexIOReader::close() {
    redis->sync_commit();
    return true;
}


//FILE *f = nullptr;
//bool need_close = false;
//
//FileIOReader(FILE *rf): f(rf) {}
//
//FileIOReader(const char * fname)
//{
//    name = fname;
//    f = fopen(fname, "rb");
//    FAISS_THROW_IF_NOT_FMT (
//            f, "could not open %s for reading: %s",
//            fname, strerror(errno));
//    need_close = true;
//}
//
//~FileIOReader() {
//    if (need_close) {
//        int ret = fclose(f);
//        FAISS_THROW_IF_NOT_FMT (
//                ret == 0, "file %s close error: %s",
//                name.c_str(), strerror(errno));
//    }
//}
//
//size_t operator()(
//        void *ptr, size_t size, size_t nitems) override {
//return fread(ptr, size, nitems, f);
//}
//
//int fileno() override {
//return ::fileno (f);
//}