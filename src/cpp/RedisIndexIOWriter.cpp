//
// Created by pletessier on 30/04/19.
//

#include <iostream>
#include "RedisIndexIOWriter.h"


RedisIndexIOWriter::RedisIndexIOWriter() {
    std::cout << "Creating index in Redis" << std::endl;
}

RedisIndexIOWriter::~RedisIndexIOWriter() {

}

size_t RedisIndexIOWriter::operator()(const void *ptr, size_t size, size_t nitems) {

    std::cout << "Writing index in Redis" << std::endl;

    return nitems;
    //fwrite(ptr, size, nitems, f);

}

