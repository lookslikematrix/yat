FROM alpine:latest

ENV SOURCE_DIRECTORY=""
ENV XDG_CACHE_HOME=.yat/software-composition-analysis/cache

RUN apk add --update --no-cache python3

RUN mkdir -p /.yat
RUN python -m venv /.yat/venv
RUN /.yat/venv/bin/pip install cyclonedx-bom

COPY run.sh /.yat/run.sh
