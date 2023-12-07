FROM python:3.11-slim

MAINTAINER Justin Flannery <juftin@juftin.com>

COPY requirements.txt /tmp/project/requirements.txt
COPY README.md /tmp/project/README.md
COPY pyproject.toml /tmp/project/pyproject.toml
COPY example_project /tmp/project/example_project

RUN pip install -r /tmp/project/requirements.txt --no-deps
RUN pip install /tmp/project && \
    rm -rf /tmp/project
