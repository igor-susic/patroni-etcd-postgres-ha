FROM ubuntu:20.04

# ENV variables setup
ENV ETCD_VER=v3.4.16
ENV ETCD_BIN=/tmp/test-etcd
ENV DOWNLOAD_URL=https://github.com/etcd-io/etcd/releases/download
ENV NODE1=172.17.0.2

# Mount data to be permanent on disk
VOLUME /etcd-data

# Run everything needed for setup
RUN apt-get update && \
    apt-get install -y curl && \
    rm -f /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz && \
    rm -rf $ETCD_BIN && \
    mkdir -p $ETCD_BIN && \
    curl -L ${DOWNLOAD_URL}/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz -o /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz && \
    tar xzvf /tmp/etcd-${ETCD_VER}-linux-amd64.tar.gz -C $ETCD_BIN --strip-components=1

# POrts that will be exposed
EXPOSE 2379 2380

# Run etcd node
CMD $ETCD_BIN/etcd \
  --data-dir=/etcd-data --name node1 \
  --initial-advertise-peer-urls http://${NODE1}:2380 --listen-peer-urls http://0.0.0.0:2380 \
  --advertise-client-urls http://${NODE1}:2379 --listen-client-urls http://0.0.0.0:2379 \
  --initial-cluster node1=http://${NODE1}:2380