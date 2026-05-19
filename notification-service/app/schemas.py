from pydantic import BaseModel

class NotificationPayload(BaseModel):
    job_id: str
    summary: str