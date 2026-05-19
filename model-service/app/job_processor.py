import json
from app.notifier import Notifier
from app.summarizer import Summarizer


class JobProcessor: 


    def __init__(self, summarizer: Summarizer, notifier:Notifier): 
        self.summarizer = summarizer
        self.notifier = notifier

    def process_job(self, data: bytes) -> str: 
        loaded = json.loads(data.decode())
        # validation etc..
        job_id = loaded['job_id']
        summary = self.summarizer.summarize_text(loaded['text'])
        self.notify(job_id=job_id, summary=summary)
        return summary
    
    def notify(self, job_id:int, summary: str): 
        self.notifier.notify(job_id=job_id, summary=summary)