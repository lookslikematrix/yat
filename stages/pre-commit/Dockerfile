FROM alpine:latest

ENV TARGET_BRANCH=origin/main
ENV XDG_CACHE_HOME=.yat/precommit/cache

RUN apk add --update --no-cache python3 bash git nodejs npm yq
RUN git config --system --add safe.directory '*'
RUN npm config set cache .yat/precommit/cache/.npm --global && npm --global cache verify

RUN mkdir -p /.yat
RUN python -m venv /.yat/venv
RUN /.yat/venv/bin/pip install pre-commit

COPY yat.yml /.yat/yat.yml
COPY run.sh /.yat/run.sh
