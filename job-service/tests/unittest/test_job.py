import json
import uuid

from app.job_creator import JobCreator
"""
- job_id exists
- job_id is valid UUID
- message is valid JSON
- message contains same job_id
- message contains original text"""




def test_creates_proper_job():

    
    text = "A wonderful serenity has taken possession of my entire soul."

    creator = JobCreator()
    job_id, job = creator.create_job(text=text)

    assert isinstance(job_id, str)
    assert isinstance(job, str)

    uuid.UUID(job_id)

    job_data = json.loads(job)

    assert job_data["job_id"] == job_id
    assert job_data["text"] == text
    