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

CMD ["python", "-m", "app.main"]
# CMD ["poetry", "run", "python", "-m", "app.main"]

#sudo docker run -d --name model-service --network textsummary-net -e RABBITMQ_HOST=rabbitmq -e RABBITMQ_PORT=5672 -e QUEUE_NAME=jobs -e NOTIFICATION_URL=http://notification-service:8001/api/notification model-service