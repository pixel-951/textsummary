from fastapi import WebSocket, WebSocketDisconnect
from app.schemas import NotificationPayload

class ConnectionManager: 


    def __init__(self):
        self.connections = {}
        self.pending_results = {}

    async def handle_connection(self, websocket: WebSocket): 
        await websocket.accept()
        job_id = await websocket.receive_text()  # browser sends job_id first
        self.connections[job_id] = websocket
        try: 
            if job_id in self.pending_results:
                await self.send(websocket=websocket, result=self.pending_results.pop(job_id), job_id=job_id)
                return
            
            # keep connection open => then what?
            while True: 
                await websocket.receive_text() 

        finally:
            self.connections.pop(job_id, None)


    async def handle_result(self, job: NotificationPayload): 
        job_id = job.job_id
        websocket = self.connections.get(job_id)
        if websocket:
            await self.send(websocket=websocket, result=job.summary, job_id=job_id)
        else:
            self.pending_results[job.job_id] = job.summary

    
    async def send(self, websocket:WebSocket, result: str, job_id:str): 
        try: 
            await websocket.send_text(result)
            await websocket.close()
        finally:
            self.connections.pop(job_id, None)
