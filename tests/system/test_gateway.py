import os

import pytest
import requests


BASE_URL = os.getenv("BASE_URL", "http://localhost:80")

# technically system test
@pytest.mark.system
def test_frontend_is_served_through_nginx():
    response = requests.get(f"{BASE_URL}/", timeout=10)

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


@pytest.mark.system
def test_job_can_be_submitted_through_nginx():
    response = requests.post(
        f"{BASE_URL}/api/job",
        json={"text": "This is an integration test."},
        timeout=20,
    )

    assert response.status_code == 202

    body = response.json()
    assert "job_id" in body
    assert body["job_id"]