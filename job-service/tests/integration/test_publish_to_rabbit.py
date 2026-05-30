import time

import pika
import pytest
import requests


JOB_SERVICE_URL = "http://localhost:18000"
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
QUEUE_NAME = "jobs"


def wait_for_job_service_ready(timeout_seconds: int = 30) -> None:
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        try:
            response = requests.get(f"{JOB_SERVICE_URL}/ready", timeout=3)
            if response.status_code == 200:
                return
        except requests.RequestException:
            pass

        time.sleep(1)

    raise RuntimeError("job-service did not become ready")


def wait_for_rabbitmq(timeout_seconds: int = 30) -> pika.BlockingConnection:
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT,
                )
            )
        except pika.exceptions.AMQPConnectionError:
            time.sleep(1)

    raise RuntimeError("RabbitMQ did not become ready")


@pytest.mark.integration
def test_job_service_publishes_valid_message_to_rabbitmq():
    wait_for_job_service_ready()

    connection = wait_for_rabbitmq()
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_purge(queue=QUEUE_NAME)

    response = requests.post(
        f"{JOB_SERVICE_URL}/api/job",
        json={"text": "integration test message"},
        timeout=10,
    )

    assert response.status_code == 202

    response_body = response.json()
    assert "job_id" in response_body
    assert response_body["job_id"]

    method_frame = None
    body = None

    for _ in range(10):
        method_frame, properties, body = channel.basic_get(
            queue=QUEUE_NAME,
            auto_ack=True,
        )

        if method_frame is not None:
            break

        time.sleep(1)

    connection.close()

    assert method_frame is not None
    assert body is not None

    decoded_body = body.decode("utf-8")
    assert "integration test message" in decoded_body