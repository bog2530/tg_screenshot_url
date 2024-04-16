FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

ENV PYTHONUNBUFFERED=true

ARG CACHEBUST=$(date +%s)

COPY [ \
  "pyproject.toml", \
  "poetry.lock", \
  "main.py", \
  "alembic.ini", \
"./"]


RUN pip install poetry

COPY . .

RUN poetry install
