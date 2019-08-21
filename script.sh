#!/bin/bash

export PYTHONUNBUFFERED=1;
export ENV_FOR_DYNACONF=default;
export MERGE_ENABLED_FOR_DYNACONF=true;
export DYNACONF_ENV_VAR=1;
export GLOBAL_ENV_FOR_DYNACONF=TARANIS;
export DYNACONF_WORKS=merge_configs;
export SILENT_ERRORS_FOR_DYNACONF=false;
export DEBUG_LEVEL_FOR_DYNACONF=WARN;
export ROOT_PATH_FOR_DYNACONF=/home/pletessier/Dev/pletessier/taranis/;
export LD_LIBRARY_PATH=/home/pletessier/Dev/pletessier/faiss/install/lib;
export LIBRARY_PATH=/home/pletessier/Dev/pletessier/faiss/install/lib;
export PYTHONPATH=/home/pletessier/Dev/pletessier/taranis/src/python:/home/pletessier/Dev/pletessier/taranis:/home/pletessier/Dev/pletessier/taranis/cmake-build-debug:/home/pletessier/Dev/pletessier/taranis/venv_debug/lib/python3.7/site-packages
#export PYTHONMALLOC=malloc

#valgrind python /home/pletessier/Dev/pletessier/taranis/src/python/app.py
valgrind --leak-check=full \
         --show-leak-kinds=all \
         --track-origins=yes \
         --verbose \
         --log-file=valgrind-out.txt \
         python /home/pletessier/Dev/pletessier/taranis/tests/test_grpc/grpc_server.py