FROM python:3.12

RUN apt-get update && apt-get install -y build-essential libpq-dev postgresql-client && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --with dev --no-root

COPY . /app

EXPOSE 5000

CMD ["sh", "-c", "until pg_isready -h db -p 5432; do echo 'Waiting for DB...'; sleep 1; done && alembic upgrade head && python run.py"]
