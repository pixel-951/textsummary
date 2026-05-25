import pika
import socket
import time


from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.job_creator import JobCreator


class QueueHandler: 

    def __init__(self, port: int=5672, host: str='localhost', queue_name: str='jobs'):
        self.job_creator = JobCreator()
        self.host = host
        self.port = port
        self.queue_name = queue_name

        self.connection = None
        self.channel = None
        

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
   
        self._connect() 
        yield 
        self._close()


    def _close(self): 
        try: 
            if self.connection and self.connection.is_open:
                self.connection.close()
        except Exception as exc: 
            print(f"{exc}")
    

    def _connect(self): 
        # create connection to queue and channel
        # sender
        while True: 
            try: 
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
                print(f"Successful connection!")
                break
            except (pika.exceptions.AMQPConnectionError, pika.exceptions.StreamLostError, socket.gaierror, OSError) as exc:
                print(f"RabbitMQ not ready yet: {exc}. Retrying in 2s...")
                time.sleep(2)
        self.channel = self.connection.channel()
        # receiver (idempotent, needs it to avoid race condition(?) such that messages do not get dropped)
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def _publish_message(self, job: str): 
        if self.channel is None or self.channel.is_closed:
            raise pika.exceptions.ChannelWrongStateError("Queue channel is not open")
        
        self.channel.basic_publish(exchange='', 
                        routing_key=self.queue_name,
                        body=job)

    def publish(self, text: str) -> dict: 
        job_id, job = self.job_creator.create_job(text)
        
        try: 
            self._publish_message(job=job)
        except (pika.exceptions.StreamLostError,
            pika.exceptions.ConnectionClosedByBroker,
            pika.exceptions.ChannelWrongStateError,
            pika.exceptions.AMQPConnectionError,
            OSError) as exc: 
            
            print(f"Connection to RabbitMQ lost, reconnecting: {exc}, Retrying...")
            self._close()
            self._connect()
            print(f"Reposting: ")
            # fine bc this will only be reached if connecting has been successful
            self._publish_message(job=job)

        return {"job_id": job_id}