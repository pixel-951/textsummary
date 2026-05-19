#!/usr/bin/env python
import pika
import time

from job_processor import JobProcessor




class QueueHandler: 

    def __init__(self, job_processor:JobProcessor, address: str='localhost', queue_name: str='jobs'):
        self.address = address
        self.queue_name = queue_name
        self.channel = self.connect().channel()

     
        self.job_processor = job_processor

    def connect(self) -> pika.BlockingConnection:
        while True:
            try:
                return pika.BlockingConnection(
                    pika.ConnectionParameters(self.address)
                )
            except Exception:
                print("Retrying...")
                time.sleep(2)

    def consume_job(self, ch, method, properties, body): # correct signature?
        # TODO: error handling
        summary = self.job_processor.process_job(body)
        print(f"Obtained summary: {summary}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
     

    def start(self) -> None: 
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.consume_job)
        self.channel.start_consuming()




