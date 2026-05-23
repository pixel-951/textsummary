import asyncio
import pika
import socket


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
        while True: 
            try: 
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
                print(f"Successful connection!")
                break
            except (pika.exceptions.AMQPConnectionError, pika.exceptions.StreamLostError, socket.gaierror) as exc:
                print(f"RabbitMQ not ready yet: {exc}. Retrying in 2s...")
                await asyncio.sleep(2)
        self.channel = self.connection.channel()
        # receiver (idempotent, needs it to avoid race condition(?) such that messages do not get dropped)
        self.channel.queue_declare(queue=self.queue_name, durable=True) 
        yield 
        if self.connection and self.connection.is_open:
            self.connection.close()
    

    def publish(self, text: str) -> dict: 
        job_id, job = self.job_creator.create_job(text)
        if self.channel is None:
            raise RuntimeError("Queue channel is not initialized")
        self.channel.basic_publish(exchange='',
                      routing_key=self.queue_name,
                      body=job)

        return {"job_id": job_id}