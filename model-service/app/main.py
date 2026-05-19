#!/usr/bin/env pyton
from job_processor import JobProcessor
from notifier import Notifier
from settings import Settings
from summarizer import Summarizer
from queue_handler import QueueHandler


settings = Settings()




summarizer = Summarizer(model=settings.model_name, max_length=settings.summary_max_length)
notifier = Notifier(host=settings.notification_url)
job_processor = JobProcessor(summarizer=summarizer, notifier=notifier)
queue_handler = QueueHandler(job_processor=job_processor, port=settings.rabbitmq_port, host=settings.rabbitmq_host, queue_name=settings.queue_name)
queue_handler.start()


# TODO: from env config read out all the configs before wiring together

# main glues everything together
# classes: summarizer (concerns itself only with summarization); queuehandler (handles )
# read env stuff like localhost dynamically instead of static
# main imports queue handler and summairzer