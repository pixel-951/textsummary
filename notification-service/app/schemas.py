from pydantic import BaseModel
from typing import Literal

class NotificationPayload(BaseModel):
    job_id: str
    summary: str


class HealthCheck(BaseModel):
    status: Literal["OK"]


class ReadinessCheck(BaseModel):
    status: Literal["READY"]