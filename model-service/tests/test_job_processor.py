"""
Unit test for model-service job_processor. Tests jobprocessor output format.
"""


import pytest


from app.job_processor import JobProcessor



class FakeSummarizer: 

    def __init__(self): 
        self.received_text = ""

    def summarize_text(self, text: str) -> str: 
        self.received_text = text
        return f"summary: {text}"

class FakeNotifier: 
    def __init__(self): 
        self.sent = False
        self.received_summary = ""
        self.job_id = 0
    
    def notify(self, job_id: str, summary: str):
        self.sent = True
        self.received_summary = summary
        self.job_id = job_id

summarizer = FakeSummarizer()
notifier = FakeNotifier()

def test_job_processor_summarizes_and_notifies():
    # use default arguments
    

    processor = JobProcessor(summarizer=summarizer, notifier=notifier)

    body = b'{"job_id": "job-123", "text": "A wonderful serenity has taken possession of my entire soul."}'
    summary = processor.process_job(body)

    assert notifier.sent is True
    assert notifier.received_summary == "summary: A wonderful serenity has taken possession of my entire soul."
    assert notifier.job_id == "job-123"

    assert summarizer.received_text == "A wonderful serenity has taken possession of my entire soul."

    assert summary == "summary: A wonderful serenity has taken possession of my entire soul."

    


def test_job_processor_fails_for_missing_text():
    processor = JobProcessor(
        summarizer=FakeSummarizer(),
        notifier=FakeNotifier(),
    )

    body = b'{"job_id": "job-123"}'

    with pytest.raises(KeyError):
        processor.process_job(body)