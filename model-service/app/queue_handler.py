#!/usr/bin/env python
import pika
import time

from app.job_processor import JobProcessor




class QueueHandler: 

    def __init__(self, job_processor:JobProcessor, port: int=5672, host: str='localhost', queue_name: str='jobs'):
        self.host = host
        self.port = port
        self.queue_name = queue_name
        self.job_processor = job_processor
        self.connection = None
        self.channel = None

    def connect(self):
        while True:
            try:
                self.connection =  pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, port=self.port)
                )
                self.channel = self.connection.channel()
                return
            except Exception:
                print("Retrying...")
                time.sleep(2)

    def consume_job(self, ch, method, properties, body): # correct signature?

        try:
            summary = self.job_processor.process_job(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"Obtained summary: {summary}")
        except Exception as exc:
            print(f"Failed to process job: {exc}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
     

    def start(self) -> None: 
        
        while True: 
            try: 
                self.connect()
                self.channel.queue_declare(queue=self.queue_name, durable=True)
                self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.consume_job)
                self.channel.start_consuming()
            except (pika.exceptions.ConnectionClosedByBroker,
                pika.exceptions.StreamLostError,
                pika.exceptions.AMQPConnectionError,
                pika.exceptions.ChannelWrongStateError) as exec: 
                print(f"Connection closed by peer, retrying: {exec}")
                time.sleep(2)
            finally:
                try:
                    if self.connection and self.connection.is_open:
                        self.connection.close()
                except Exception:
                    pass

           
                




