ARG BASE_IMAGE=nvidia/cuda:12.1.1-devel-ubuntu22.04
FROM ${BASE_IMAGE} as dev-base

WORKDIR /

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV DEBIAN_FRONTEND noninteractive\
    SHELL=/bin/bash

RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt install --yes --no-install-recommends g++ git wget curl bash libgl1 software-properties-common openssh-server && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt install python3.11-dev -y --no-install-recommends && \
	ln -s /usr/bin/python3.11 /usr/bin/python && \
	rm /usr/bin/python3 && \
	ln -s /usr/bin/python3.11 /usr/bin/python3 && \
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
	python get-pip.py &&  \
    apt-get autoclean

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

COPY requirements.txt requirements.txt
RUN python3.11 -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY file_kit.py file_kit.py
COPY model_preloader.py model_preloader.py
RUN python3.11 model_preloader.py
COPY worker.py worker.py

CMD python3.11 -u worker.py | tee log.txt