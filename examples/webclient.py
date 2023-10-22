import asyncio
import websockets
import threading

def run_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def send_message():
    uri = "ws://127.0.0.1:8000"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello from the client!")

def start_websocket_client():
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=run_loop, args=(loop,))
    t.start()

    asyncio.run_coroutine_threadsafe(send_message(), loop)

# Starting the WebSocket client
start_websocket_client()
