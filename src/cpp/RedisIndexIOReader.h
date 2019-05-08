//
// Created by pletessier on 05/05/19.
//

#ifndef CPP_TARANIS_REDISINDEXIOREADER_H
#define CPP_TARANIS_REDISINDEXIOREADER_H


class RedisIndexIOReader: public IOReader {

public:
    RedisIndexIOReader(cpp_redis::client* redis, std::string db_name, std::string index_name);

    ~RedisIndexIOReader();

    size_t operator()(void *ptr, size_t size, size_t nitems) override;

    bool close();

private:
    cpp_redis::client* redis;
    std::string key;
    uint8_t * data;

};


#endif //CPP_TARANIS_REDISINDEXIOREADER_H
