#!/usr/bin/env python
import requests
 

class Notifier: 
    def __init__(self, host:str="http://localhost:8001/api/notification"):
        self.host = host

    def notify(self, job_id: str, summary: str):
        requests.post(
            self.host,
            json={"job_id": job_id, "summary": summary}
        , timeout=5)
        print(f"sent notification with summary: {summary}")


    
  

 