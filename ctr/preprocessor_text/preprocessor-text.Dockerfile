# ARG MECAB_VERSION=0.996
# ARG IPADIC_VERSION=2.7.0-20070801
# ARG mecab_url=https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE
# ARG ipadic_url=https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM
# ARG build_deps='curl git bash file sudo openssh'
# ARG dependencies='openssl'

# ARG PYTHON_IMAGE_VERSION=3.8.1-alpine
FROM debian:buster as mecab_build
LABEL mecab_build=true
WORKDIR /tmp
RUN apt update && apt install -y git make curl xz-utils file sudo wget gcc g++ 

# RUN apk --update add --virtual build-dependencies \
#     git \
#     gcc \
#     g++ \
#     make 
# RUN apk --update add --virtual neologd-dependencies \
#     bash \
#     curl \
#     file \
#     openssl \
#     sudo 
RUN git clone https://github.com/taku910/mecab.git \
    && cd mecab/mecab \
    && ./configure  --enable-utf8-only  --with-charset=utf8 \
    && sudo ldconfig \
    && make \
    && make check \
    && make install

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
    && sudo ldconfig \
    && mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y 
# RUN cd /tmp \
#     && rm -rf \
#     && mecab \
#     && mecab-ipadic-neologd

RUN git clone https://github.com/facebookresearch/fastText.git \
    && cd fastText  \
    && make 


# FROM alpine:3.9.5 as mecab_build
# LABEL mecab_build=true
# WORKDIR /tmp
# RUN apk --update add --virtual build-dependencies \
#     git \
#     gcc \
#     g++ \
#     make 
# RUN apk --update add --virtual neologd-dependencies \
#     bash \
#     curl \
#     file \
#     openssl \
#     sudo 
# RUN git clone https://github.com/taku910/mecab.git \
#     && cd mecab/mecab \
#     && ./configure  --enable-utf8-only  --with-charset=utf8 \
#     && make \
#     && make check \
#     && make install
#     # && ldconfig 
# RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
#     && mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y 
# # RUN cd /tmp \
# #     && rm -rf \
# #     && mecab \
# #     && mecab-ipadic-neologd

# RUN git clone https://github.com/facebookresearch/fastText.git \
#     && cd fastText  \
#     && make 

# # RUN rm -rf \
#     # && mecab \
#     # && mecab-ipadic-neologd \
#     # && fastText

# RUN apk del build-dependencies  neologd-dependencies


# FROM ubuntu:18.04  as preprocessor_text

FROM python:3.8.3-buster as preprocessor_text

COPY --from=mecab_build /usr/local /usr/local
COPY --from=mecab_build /tmp/fastText /home/fastText

# sklearn dependencies
RUN apt update && apt install -y libfreetype6-dev libatlas-base-dev liblapack-dev gfortran 

# mecab dependecies
RUN apt update \
    && apt install -y build-essential  manpages-dev 

# RUN apt install -y python3.8 python3-pip
# # RUN python3.8 -m pip install pyinotify

RUN pip install --upgrade pip setuptools wheel \
    'tqdm==4.46.0' \
    'emoji==0.5.4' \
    'neologdn==0.4' \
    'mecab-python3==0.7' \
    'scikit-learn==0.23.1' \
    'pandas' \
    "pyyaml" \
    && cd /home/fastText \
    && pip install . 

# # dev
# RUN apt-get install -y bash-completion vim

# RUN apt-get clean
