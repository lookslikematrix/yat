FROM alpine:latest

ENV SOURCE_DIRECTORY=""
ENV YAT_RELEASE_NAME=""
ENV YAT_RELEASE_VERSION=""
ENV XDG_CACHE_HOME=.yat/software-composition-analysis/cache
ENV SYFT_CACHE_DIR=.yat/software-composition-analysis/cache

RUN apk add --update --no-cache yq curl
RUN curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin

COPY yat.yml /.yat/yat.yml
COPY run.sh /.yat/run.sh
