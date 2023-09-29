FROM python:3.11-slim

MAINTAINER {{ cookiecutter.full_name }} <{{ cookiecutter.email }}>

COPY requirements.txt /tmp/project/requirements.txt
COPY README.md /tmp/project/README.md
COPY pyproject.toml /tmp/project/pyproject.toml
COPY {{ cookiecutter.project_slug }} /tmp/project/{{ cookiecutter.project_slug }}

RUN pip install -r /tmp/project/requirements.txt --no-deps
RUN pip install /tmp/project && \
    rm -rf /tmp/project
