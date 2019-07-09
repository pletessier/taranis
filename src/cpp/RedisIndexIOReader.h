// Copyright (C) 2019 Pierre Letessier
// This source code is licensed under the BSD 3 license found in the
// LICENSE file in the root directory of this source tree.

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
