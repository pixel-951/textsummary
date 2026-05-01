#!/usr/bin/env python
import json
import pika
import uuid

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

"""
Entry to the backend services. Accepts requests and delegates to other services. 

Routes: 
POST /job
GET / serves frontend

"""



@asynccontextmanager
async def lifespan(app: FastAPI):
    # create queue connection and channel on startup such that there can be potential error handling and reconnecting
    global channel, connection

    # create connection to queue and channel
    # sender
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # receiver (idempotent, needs it to avoid race condition(?) such that messages do not get dropped)
    channel.queue_declare(queue='jobs', durable=True) # not sure if needed, will be created in model-service as well
    yield 
   
    #connection.close()


app = FastAPI(lifespan=lifespan)

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
    job_id = str(uuid.uuid4())
    message = json.dumps({"job_id": job_id, "text": text})
    channel.basic_publish(exchange='',
                      routing_key='jobs',
                      body=message)

    
    return {"job_id": job_id}



