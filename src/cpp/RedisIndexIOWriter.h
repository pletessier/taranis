//
// Created by pletessier on 30/04/19.
//

#ifndef CPP_TARANIS_REDISINDEXIOWRITER_H
#define CPP_TARANIS_REDISINDEXIOWRITER_H

#include <faiss/AuxIndexStructures.h>

using namespace faiss;

class RedisIndexIOWriter : public IOWriter {

//    FILE *f = nullptr;
    bool need_close = false;

public:
    RedisIndexIOWriter();

    ~RedisIndexIOWriter();


    size_t operator()(const void *ptr, size_t size, size_t nitems) override;
};


#endif //CPP_TARANIS_REDISINDEXIOWRITER_H
