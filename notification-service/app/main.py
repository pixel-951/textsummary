#!/usr/bin/env python

from fastapi import FastAPI, WebSocket

from app.connection_manager import ConnectionManager
from app.schemas import NotificationPayload

"""
Entry to the backend services. Accepts requests and delegates to other services. 

Routes: 
POST /api/notification
ws websocket

"""





server = FastAPI()

connection_manager = ConnectionManager()

@server.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    await connection_manager.handle_connection(websocket=websocket)



@server.post("/api/notification")
async def receive_notification(job: NotificationPayload):

    await connection_manager.handle_result(job=job)
    return {"status": "ok"}
   

    




