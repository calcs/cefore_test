# Dockerfile
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# Build deps
RUN apt-get update && apt-get install -y \
    build-essential git autoconf automake libtool pkg-config cmake \
    libssl-dev libpcap-dev libxml2-dev libcurl4-openssl-dev \
    python3 python3-dev python3-pip python3-setuptools python3-wheel python3-venv \
 && rm -rf /var/lib/apt/lists/*

# Cefore（キャッシュ/マネージャ有効でビルド）
RUN git clone --depth=1 https://github.com/cefore/cefore.git /opt/cefore \
 && cd /opt/cefore \
 && ./configure --enable-csmgr --enable-cache \
 && make -j"$(nproc)" \
 && make install \
 && ldconfig

# Python 側（cefpyco が内部で python -m build を使う）
RUN pip3 install --no-cache-dir setuptools wheel click numpy build requests

# Python: cefpyco + requests
RUN git clone --depth=1 https://github.com/cefore/cefpyco.git /opt/cefpyco \
 && cd /opt/cefpyco && cmake . && make -j"$(nproc)" && make install

# ランタイム探索パス
RUN printf "/usr/local/lib\n/usr/local/lib/cefore\n" > /etc/ld.so.conf.d/cefore.conf && ldconfig

ENV USER=root HOME=/root CEFORE_DIR=/usr/local
WORKDIR /workspace
