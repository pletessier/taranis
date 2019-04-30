cmake_minimum_required(VERSION 3.13)
project(cpp_taranis)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp -g -ggdb -O0")

find_package(PkgConfig)
find_package(pybind11 REQUIRED)


set(ENV{PKG_CONFIG_PATH}  "../../cpp_redis/cmake-build-release/install/lib/pkgconfig")

pkg_check_modules(CPP_REDIS cpp_redis REQUIRED)

include_directories(SYSTEM ../faiss/install/include ${CPP_REDIS_INCLUDEDIR})
link_directories(../faiss/install/lib ${CPP_REDIS_LIBDIR})

set(source_files src/cpp/taranis.cpp src/cpp/RedisIndexIOWriter.cpp)

pybind11_add_module(cpp_taranis SHARED ${source_files})
target_link_libraries(cpp_taranis PRIVATE libfaissd.a libopenblas.so libfmt.so ${cpp_redis_LIBRARIES} tacopie.a)