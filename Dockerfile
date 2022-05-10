# syntax = docker/dockerfile:1-experimental
ARG ALPINE_VERSION=3.15

FROM alpine:${ALPINE_VERSION} as python_base

RUN set -euxo pipefail ;\
    apk add --no-cache --update python3 py3-pip py3-wheel dumb-init;\
    pip install --no-cache --upgrade pip flit ;\
    ln -s /usr/bin/python3 /usr/bin/python

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD "/bin/bash"

FROM python_base as python_builder

ADD . /untropy

RUN set -ex \
    \
    && cd /untropy \
    && ls \
    && flit build --format wheel


FROM alpine:${ALPINE_VERSION}

ENV PYTHONUNBUFFERED 1

RUN set -euxo pipefail ;\
    apk add --update --no-cache \
    ca-certificates openssh-client sshpass dumb-init su-exec \
    python3 py3-pip py3-wheel py3-openssl py3-aiohttp py3-netifaces py3-bcrypt py3-yaml \
    py3-pynacl py3-pyrsistent py3-ruamel.yaml.clib \
    jq \
    git \
    openssl \
    bash \
    curl \
    make \
    docker \
    libstdc++ \
    unzip \
    patch \
    tar ;\
    pip install --no-cache --upgrade pip ;\
    rm -rf /var/cache/apk/* ;\
    rm -rf /root/.cache ;\
    ln -s /usr/bin/python3 /usr/bin/python

COPY --from=python_builder /untropy/dist /wheels

RUN set -euxo pipefail ;\
    apk add --no-cache --update --virtual .build-deps python3-dev build-base libffi-dev openssl-dev ;\
    PIP_FIND_LINKS="/wheels" pip install /wheels/untropy* ;\
    pip cache purge ;\
    apk del --no-cache --purge .build-deps ;\
    rm -rf /var/cache/apk/* ;\
    rm -rf /root/.cache ;\
    ssh-keygen -q -t ed25519 -N '' -f /root/.ssh/id_ed25519 ;\
    mkdir -p ~/.ssh && echo "Host *" > ~/.ssh/config && echo " StrictHostKeyChecking no" >> ~/.ssh/config ;\
    adduser -s /bin/ash -u 1000 -D -h /untropy untropy

WORKDIR /untropy

SHELL ["/bin/bash", "-c"]

ENTRYPOINT []
