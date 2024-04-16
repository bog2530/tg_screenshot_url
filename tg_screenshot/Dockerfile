FROM python:3.10-slim
ENV PYTHONUNBUFFERED=true

ARG CACHEBUST=$(date +%s)

COPY [ \
  "pyproject.toml", \
  "poetry.lock", \
  "main.py", \
  "load.png", \
"./"]


RUN pip install poetry

COPY . .

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "main.py"]

#FROM python:3.10-buster
#
#RUN pip install poetry
#
#COPY . .
#
#RUN poetry install
#
#ENTRYPOINT ["poetry", "run", "python", "main.py"]