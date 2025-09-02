# Dockerfile
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# 基本ツール + 依存
RUN apt-get update && apt-get install -y \
    build-essential git cmake pkg-config autoconf automake libtool \
    libssl-dev libpcap-dev libxml2-dev libcurl4-openssl-dev \
    python3 python3-dev python3-pip python3-setuptools python3-wheel python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Cefore 本体
RUN git clone --depth=1 https://github.com/cefore/cefore.git /opt/cefore \
 && cd /opt/cefore \
 && ./configure \
 && make -j"$(nproc)" \
 && make install

# Python 側（cefpyco が内部で python -m build を使う）
RUN pip3 install --no-cache-dir setuptools wheel click numpy build requests

# cefpyco（別リポジトリ）
RUN git clone --depth=1 https://github.com/cefore/cefpyco.git /opt/cefpyco \
 && cd /opt/cefpyco \
 && cmake . \
 && make -j"$(nproc)" \
 && make install

# ライブラリ探索パスを恒久化
RUN printf "/usr/local/lib\n/usr/local/lib/cefore\n" > /etc/ld.so.conf.d/cefore.conf && ldconfig

# 便利な既定環境（必要なら上書き可）
ENV USER=root HOME=/root CEFORE_DIR=/usr/local

WORKDIR /workspace
# CMD/ENTRYPOINT は設定しない（手動運用前提）
