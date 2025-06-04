FROM python:alpine

ENV TARGET_BRANCH=origin/main
ENV XDG_CACHE_HOME=.yat/precommit/cache

RUN apk add git
RUN git config --global --add safe.directory '*'

RUN mkdir -p /.yat
RUN python -m venv /.yat/venv
RUN /.yat/venv/bin/pip install pre-commit

COPY run.sh /.yat/run.sh

CMD [ "/bin/sh", "/.yat/run.sh" ]
