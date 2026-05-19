import json
from notifier import Notifier
from summarizer import Summarizer


class JobProcessor: 


    def __init__(self, summarizer: Summarizer, notifier:Notifier): 
        self.summarizer = summarizer
        self.notifier = notifier
        self.current_jobid = 0

    def process_job(self, data: json) -> str: 
        loaded = json.loads(data.decode())
        # validation etc..
        self.current_jobid = loaded['job_id']
        summary = self.summarizer.summarize_text(loaded['text'])
        self.notify(summary=summary)
        return summary
    
    def notify(self, summary: str): 
        self.notifier.notify(job_id=self.current_jobid, summary=summary)