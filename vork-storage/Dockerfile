ARG BUILD_FROM
FROM ${BUILD_FROM}

# vØrk storage's static programs from a release of
# github.com/vooteleaer/vork-storage, checked against their SHA-256 here, at
# build time.
ARG BUILD_ARCH
ARG STORAGE_RELEASE
ARG STORAGE_SHA256_AMD64
ARG STORAGE_SHA256_AARCH64
RUN set -e; \
    case "${BUILD_ARCH}" in \
      amd64) file=vork-storage-linux-x86_64.tar.gz; sum="${STORAGE_SHA256_AMD64}" ;; \
      aarch64) file=vork-storage-linux-aarch64.tar.gz; sum="${STORAGE_SHA256_AARCH64}" ;; \
      *) echo "no vØrk storage build for ${BUILD_ARCH}"; exit 1 ;; \
    esac; \
    wget -qO /tmp/s.tgz "https://github.com/vooteleaer/vork-storage/releases/download/${STORAGE_RELEASE}/${file}"; \
    echo "${sum}  /tmp/s.tgz" | sha256sum -c -; \
    mkdir -p /opt/vork-storage; \
    tar xzf /tmp/s.tgz -C /opt/vork-storage; \
    rm /tmp/s.tgz

COPY run.sh /run.sh
RUN chmod 755 /run.sh
CMD ["/run.sh"]
