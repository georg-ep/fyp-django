FROM python:3.9
LABEL MAINTAINER="George Patterson"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y dist-upgrade
RUN apt install -y netcat

COPY ./requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt


RUN mkdir /app
WORKDIR /app
COPY ./app /app
COPY ./scripts /scripts
RUN mkdir /tmp/runtime-user
RUN PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

ENTRYPOINT ["/scripts/server_run.sh"]

