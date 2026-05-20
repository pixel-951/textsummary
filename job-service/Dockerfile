# poetry install, poetry activate, use the env with entry to fastapi env to start server

# use python image because we dont need OS level control
FROM python:3.11-slim 

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1


WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

# add user so container is not root
RUN useradd --create-home appuser

# copy app dir and apply user permissions
COPY --chown=appuser:appuser app ./app
USER appuser

CMD ["uvicorn", "app.main:server", "--host", "0.0.0.0", "--port", "8000"]

# sudo docker run --rm -d --name job-service --network textsummary-net -p 8000:8000 -e RABBITMQ_HOST=rabbitmq -e RABBITMQ_PORT=5672 -e QUEUE_NAME=jobs job-service
# rabbit: sudo docker run -d --name rabbitmq --network textsummary-net -p 5672:5672 -p 15672:15672 rabbitmq:3-management