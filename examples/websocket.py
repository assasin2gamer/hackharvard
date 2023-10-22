import asyncio
import websockets
import datetime

async def send_messages(websocket, path):
    while True:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"Server Time: {current_time}"
        await websocket.send(message)
        await asyncio.sleep(1)  # send a message every 1 second

start_server = websockets.serve(send_messages, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
