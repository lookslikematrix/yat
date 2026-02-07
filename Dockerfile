FROM python:slim

COPY yat /opt/yat
WORKDIR /opt

CMD ["python", "-m", "yat"]
