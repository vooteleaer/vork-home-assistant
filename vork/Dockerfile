ARG BUILD_FROM
FROM ${BUILD_FROM}

# The node is a release's static binary (github.com/vooteleaer/vork),
# checked against its SHA-256 here, at build time.
ARG BUILD_ARCH
ARG VORK_RELEASE
ARG VORK_SHA256_AMD64
ARG VORK_SHA256_AARCH64
RUN set -e; \
    case "${BUILD_ARCH}" in \
      amd64) file=vork-linux-x86_64; sum="${VORK_SHA256_AMD64}" ;; \
      aarch64) file=vork-linux-aarch64; sum="${VORK_SHA256_AARCH64}" ;; \
      *) echo "no vØrk build for ${BUILD_ARCH}"; exit 1 ;; \
    esac; \
    apk add --no-cache iproute2 iptables; \
    wget -qO /usr/bin/vork "https://github.com/vooteleaer/vork/releases/download/${VORK_RELEASE}/${file}"; \
    echo "${sum}  /usr/bin/vork" | sha256sum -c -; \
    chmod 755 /usr/bin/vork

COPY run.sh /run.sh
RUN chmod 755 /run.sh
CMD ["/run.sh"]
