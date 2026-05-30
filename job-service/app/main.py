#!/usr/bin/env python
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.queue_handler import QueueHandler
from app.schemas import JobCreateRequest, JobCreateResponse, HealthCheck, ReadinessCheck
from app.settings import settings

"""
Entry to the backend services. Accepts requests and delegates to other services. 

Routes: 
POST /job
GET / serves frontend

"""

# TODO gets settings


# TODO arguments: port, host, queue name
queue_handler = QueueHandler(host=settings.rabbitmq_host,
    port=settings.rabbitmq_port,
    queue_name=settings.queue_name)


server = FastAPI(lifespan=queue_handler.lifespan)

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@server.post("/api/job", response_model=JobCreateResponse)
async def add_job(request: JobCreateRequest):
    # TODO: validate input, create job object, add to queue, return error code
    print(f"Adding {request.text} to queue.")
 
    return queue_handler.publish(text=request.text)


server.get("/health", status_code=status.HTTP_200_OK, response_model=HealthCheck)
async def health_check():
    return HealthCheck(status="OK")


@server.get("/ready", status_code=status.HTTP_200_OK, response_model=ReadinessCheck)
async def readiness_check():
    if not queue_handler.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RabbitMQ connection is not ready",
        )

    return ReadinessCheck(status="READY")