FROM python:3.7.3-slim-stretch

RUN apt-get update -y && apt-get install -y cmake cmake-data build-essential pkg-config wget unzip libopenblas-dev libfmt3-dev git

WORKDIR /opt/

ARG http_proxy
ARG https_proxy
ARG no_proxy

RUN wget https://github.com/cpp-redis/cpp_redis/archive/4.3.1.zip -O cpp_redis.zip && \
    unzip cpp_redis.zip && \
    cd cpp_redis-4.3.1 && \
    wget https://github.com/Cylix/tacopie/archive/3.2.0.zip -O tacopie.zip && \
    unzip tacopie.zip -d tacopie && \
    mv tacopie/*/* tacopie/ && \
    mkdir build && \
    cd build && \
    cmake -DBUILD_SHARED_LIBS=ON ../ && \
    make -j4 && \
    make install

RUN wget https://github.com/facebookresearch/faiss/archive/v1.5.3.zip -O faiss.zip && \
    unzip faiss.zip && \
    mv faiss-1.5.3 faiss && \
    cd faiss && \
    ./configure --without-cuda && \
    make -j4 && \
    make install

RUN wget https://github.com/pybind/pybind11/archive/v2.2.4.zip -O pybind11.zip && \
    unzip pybind11.zip && \
    mv pybind11-2.2.4 pybind11 && \
    cd pybind11 && \
    mkdir build && \
    cd build && \
    pip install pytest && \
    cmake ../ && \
    make -j4 && \
    make install

RUN wget https://github.com/fmtlib/fmt/archive/5.3.0.zip -O fmtlib.zip && \
    unzip fmtlib.zip && \
    cd fmt-5.3.0 && \
    mkdir build && \
    cd build && \
    cmake -DBUILD_SHARED_LIBS=ON ../ && \
    make -j4 && \
    make install

ENV PYTHONPATH=/opt/taranis/:/opt/taranis/src/python:/opt/taranis/src/python/models:/opt/taranis/build/

WORKDIR /opt/taranis

COPY . .

RUN mkdir build && cd build && cmake ../ && make

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-W", "ignore::DeprecationWarning", "-W", "ignore::ImportWarning", "src/python/app.py"]



