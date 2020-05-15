FROM python:3.6.4-slim-stretch

RUN apt-get update && \
    apt-get -y install sudo \
    git \
    gcc \
    g++ \
    make \
    curl \
    xz-utils \
    liblzma-dev \
    file 
    # mecab-ipadic \
    # mecab-ipadic-utf8

# RUN mkdir -p /opt/downloads && \
#     cd /opt/downloads && \
#     git clone https://github.com/taku910/mecab.git && \
#     git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git

# RUN cd /opt/downloads/mecab/mecab && \
#     ./configure  --enable-utf8-only && \
#     make && \
#     make check && \
#     make install

# RUN apt-get -y install 
# RUN cd /opt/downloads/mecab-ipadic-neologd && \
#     ./bin/install-mecab-ipadic-neologd -n -y

RUN pip install gensim mecab-python3

WORKDIR /usr/src/app/

ENTRYPOINT tail -f /dev/null