ARG BASE_IMAGE=nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04
FROM ${BASE_IMAGE} as dev-base

WORKDIR /src

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV DEBIAN_FRONTEND noninteractive\
    SHELL=/bin/bash

RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt install --yes --no-install-recommends\
    wget\
    bash\
    openssh-server &&\
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3.11 -y
RUN apt-get install python3-pip -y
RUN apt-get install python3.11-distutils -y

RUN apt-get install python3.11-dev -y
RUN apt-get install python3.11-venv -y
RUN python3.11 -m venv /venv
ENV PATH=/venv/bin:$PATH

RUN python3.11 -m pip install --upgrade pip setuptools wheel
RUN python3.11 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
RUN python3.11 -m pip install runpod
RUN python3.11 -m pip install numpy
RUN python3.11 -m pip install opencv-contrib-python
RUN python3.11 -m pip install pillow
RUN python3.11 -m pip install moviepy
RUN python3.11 -m pip install cupy-cuda12x
RUN python3.11 -m pip install accelerate
RUN python3.11 -m pip install python-multipart
RUN python3.11 -m pip install fortuna
RUN python3.11 -m pip install transformers
RUN python3.11 -m pip install diffusers

ADD model_preloader.py /src/
RUN python3.11 model_preloader.py
ADD start.py /src/

CMD [ "python3.11", "-u", "start.py" ]