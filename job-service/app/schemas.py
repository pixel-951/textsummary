from pydantic import BaseModel, Field
from typing import Literal


class JobCreateRequest(BaseModel):
    text: str = Field(min_length=1)


class JobCreateResponse(BaseModel):
    job_id: str

class HealthCheck(BaseModel):
    status: Literal["OK"]


class ReadinessCheck(BaseModel):
    status: Literal["READY"]