#!/usr/bin/env python
import pika
import time

from app.job_processor import JobProcessor




class QueueHandler: 

    def __init__(self, job_processor:JobProcessor, port: int=5672, host: str='localhost', queue_name: str='jobs'):
        self.host = host
        self.port = port
        self.queue_name = queue_name
        self.channel = self.connect().channel()

     
        self.job_processor = job_processor

    def connect(self) -> pika.BlockingConnection:
        while True:
            try:
                return pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, port=self.port)
                )
            except Exception:
                print("Retrying...")
                time.sleep(2)

    def consume_job(self, ch, method, properties, body): # correct signature?
        # TODO: error handling
        summary = self.job_processor.process_job(body)
        print(f"Obtained summary: {summary}")

        try:
            summary = self.job_processor.process_job(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as exc:
            print(f"Failed to process job: {exc}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
     

    def start(self) -> None: 
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.consume_job)
        self.channel.start_consuming()




