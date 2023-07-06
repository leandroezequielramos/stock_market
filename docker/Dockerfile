FROM python:3.10.12

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip && pip install poetry==1.5.1


RUN poetry config virtualenvs.create false

COPY src app
COPY README.md /app
WORKDIR /app

COPY poetry.lock pyproject.toml ./
COPY alembic /alembic

RUN poetry install

EXPOSE 8000
CMD ["poetry", "run", "start"]