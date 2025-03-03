import asyncio
import websockets

async def echo(websocket, path):
    print("Client connected")
    async for message in websocket:
        print(f"Received: {message}")
        await websocket.send(f"Echo: {message}")

# Start the server
start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server started on ws://localhost:8765")
asyncio.get_event_loop().run_forever()

