from pydantic import BaseModel, Field


class JobCreateRequest(BaseModel):
    text: str = Field(min_length=1)


class JobCreateResponse(BaseModel):
    job_id: str