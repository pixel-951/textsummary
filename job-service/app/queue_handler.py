import pika


from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.job_creator import JobCreator


class QueueHandler: 

    def __init__(self, port: int=5672, host: str='localhost', queue_name: str='jobs'):
        self.job_creator = JobCreator()
        self.host = host
        self.port = port
        self.queue_name = queue_name
        

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
   

        # create connection to queue and channel
        # sender
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
        self.channel = self.connection.channel()
        # receiver (idempotent, needs it to avoid race condition(?) such that messages do not get dropped)
        self.channel.queue_declare(queue=self.queue_name, durable=True) 
        yield 
        #self.connection.close()
    

    def publish(self, text: str) -> dict: 
        job_id, job = self.job_creator.create_job(text)
        self.channel.basic_publish(exchange='',
                      routing_key=self.queue_name,
                      body=job)

        return {"job_id": job_id}