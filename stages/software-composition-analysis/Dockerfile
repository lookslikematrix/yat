FROM alpine:latest

ENV SOURCE_DIRECTORY=""
ENV YAT_RELEASE_NAME=""
ENV YAT_RELEASE_VERSION=""
ENV XDG_CACHE_HOME=.yat/software-composition-analysis/cache

RUN apk add --update --no-cache python3 yq

RUN mkdir -p /.yat
RUN python -m venv /.yat/venv
RUN /.yat/venv/bin/pip install cyclonedx-bom

COPY yat.yml /.yat/yat.yml
COPY run.sh /.yat/run.sh
