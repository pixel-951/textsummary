#!/usr/bin/env python
import json
import pika
import requests
import time

from transformers import pipeline




""" Polls for jobs in the queue. Takes jobs, runs them through summarization model and publishes to notification service. Also stores the summarized texts in the database. 
"""


def connect():
    while True:
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters('localhost')
            )
        except Exception:
            print("Retrying...")
            time.sleep(2)

def notify(job_id: str, summary: str):
    requests.post(
        "http://localhost:8002/api/notification",
        json={"job_id": job_id, "summary": summary}
    )
    print(f"sent notification with summary: {summary}")

def process_text(ch, method, properties, body):
    data = json.loads(body.decode())
    print(f"Processing job: {data['job_id']} with data: {data['text']}")
    result = summarizer(data['text'], max_length=130, min_length=30)
    summary = result[0]['summary_text']
    
    #print(f"Summarized text: {summary}") # post to notification service which keeps connections with clients; write to database, for now just the text and job_id?
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    # send POST to notificaiton service
    notify(job_id=data['job_id'], summary=summary)

    # store summarized text + job_id in database (or rather send to storage service)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn") # where weights?


connection = connect()
channel = connection.channel()
channel.queue_declare(queue='jobs', durable=True)
channel.basic_consume(queue='jobs', on_message_callback=process_text)
channel.start_consuming()


