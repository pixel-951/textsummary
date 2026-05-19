#!/usr/bin/env python
from job_processor import JobProcessor
from notifier import Notifier
from summarizer import Summarizer
from queue_handler import QueueHandler





summarizer = Summarizer()
notifier = Notifier()
job_processor = JobProcessor(summarizer=summarizer, notifier=notifier)
queue_handler = QueueHandler(job_processor=job_processor, address='localhost', queue_name='jobs')
queue_handler.start()


# TODO: from env config read out all the configs before wiring together

# main glues everything together
# classes: summarizer (concerns itself only with summarization); queuehandler (handles )
# read env stuff like localhost dynamically instead of static
# main imports queue handler and summairzer