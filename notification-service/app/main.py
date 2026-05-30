#!/usr/bin/env python

from fastapi import FastAPI, WebSocket, status

from app.connection_manager import ConnectionManager
from app.schemas import NotificationPayload, HealthCheck, ReadinessCheck

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



@server.post("/api/notification", status_code=status.HTTP_202_ACCEPTED,)
async def receive_notification(job: NotificationPayload):

    await connection_manager.handle_result(job=job)
    return {"status": "ok"}
   

    
@server.get("/health", status_code=status.HTTP_200_OK, response_model=HealthCheck)
async def health_check():
    return HealthCheck(status="OK")


@server.get("/ready", status_code=status.HTTP_200_OK, response_model=ReadinessCheck)
async def readiness_check():
    return ReadinessCheck(status="READY")



