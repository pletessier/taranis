cmake_minimum_required(VERSION 3.7)
project(cpp_taranis)

#set(PYTHON_EXECUTABLE /home/pletessier/Dev/pletessier/taranis/venv_debug/bin/python)

set(CMAKE_CXX_STANDARD 11)

#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp -g -ggdb -O0")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp -O3")

find_package(PkgConfig)
find_package(pybind11 REQUIRED)


set(ENV{PKG_CONFIG_PATH}  "${PROJECT_SOURCE_DIR}/../cpp_redis/cmake-build-release/install/lib/pkgconfig")

pkg_check_modules(CPP_REDIS cpp_redis REQUIRED)

include_directories(SYSTEM ../faiss/install/include ${CPP_REDIS_INCLUDEDIR})
link_directories(../faiss/install/lib ${CPP_REDIS_LIBDIR})

set(source_files src/cpp/RedisService.cpp  src/cpp/RedisIndexIOWriter.cpp src/cpp/SearchResult.cpp src/cpp/FaissWrapper.cpp src/cpp/taranis.cpp)


pybind11_add_module(cpp_taranis SHARED ${source_files})
#target_link_libraries(cpp_taranis PRIVATE libfaissd.a libopenblas.so libfmt.so ${CPP_REDIS_LIBRARIES} tacopie.a)
target_link_libraries(cpp_taranis PRIVATE libfaiss.so libopenblas.so libfmt.so ${CPP_REDIS_LIBRARIES} tacopie.so)
