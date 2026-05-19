import json
import uuid

class JobCreator: 

    def create_job(self, text: str) -> tuple[str, str]: 
        job_id = str(uuid.uuid4())
        job = json.dumps({"job_id": job_id, "text": text}) 
        return job_id, job

