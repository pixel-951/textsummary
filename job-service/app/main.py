#!/usr/bin/env python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.queue_handler import QueueHandler
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


app = FastAPI(lifespan=queue_handler.lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/job")
async def add_job(text: str):
    # TODO: validate input, create job object, add to queue, return error code
    print(f"Adding {text} to queue.")
 
    return queue_handler.publish(text=text)


# queue_handler: owns channel and connection; declares queue and publishes job to it; uses job_processor 
# job_processor: receives text string, returns json byte string with job_id
