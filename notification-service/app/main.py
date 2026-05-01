#!/usr/bin/env python
import json

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

"""
Entry to the backend services. Accepts requests and delegates to other services. 

Routes: 
POST /api/notification
ws websocket

"""

class NotificationPayload(BaseModel):
    job_id: str
    summary: str



app = FastAPI()

connections = {}
pending_results = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    job_id = await websocket.receive_text()  # browser sends job_id first
    connections[job_id] = websocket

    if job_id in pending_results:
        await websocket.send_text(pending_results.pop(job_id))
        del pending_results[job_id]
        return
    
    # keep connection open
    await websocket.receive_text() 



@app.post("/api/notification")
async def receive_notification(data: NotificationPayload):
    websocket = connections.get(data.job_id)
    if websocket:
        await websocket.send_text(data.summary)
    else:
        # WebSocket not registered yet, store for later
        pending_results[data.job_id] = data.summary
    return {"status": "ok"}
   

    




