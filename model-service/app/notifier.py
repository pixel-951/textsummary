#!/usr/bin/env python
import requests
 

class Notifier: 
    def __init__(self, address:str="http://localhost:8001/api/notification"):
        self.address = address

    def notify(self, job_id: str, summary: str):
        requests.post(
            self.address,
            json={"job_id": job_id, "summary": summary}
        , timeout=5)
        print(f"sent notification with summary: {summary}")


    
  

 