import asyncio
import websockets

async def test():
    async with websockets.connect("ws://localhost:8002/ws") as ws:
        await ws.send("9e2cdc3c-9e45-422e-ab31-26f16167c47f")
        print("Waiting for result...")
        result = await ws.recv()
        print(f"Received: {result}")

asyncio.run(test())