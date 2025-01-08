import asyncio
import websockets

async def communicate():
    uri = "ws://localhost:5000/reverse"
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter a message: ")
            await websocket.send(message)
            print(f"Sent: {message}")

            response = await websocket.recv()
            print(f"Received: {response}")

asyncio.run(communicate())

