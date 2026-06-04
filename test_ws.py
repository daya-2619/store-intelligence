import asyncio
import websockets

async def test():
    try:
        async with websockets.connect('ws://127.0.0.1:8000/websocket/live/Store_2') as ws:
            print('Connected!')
            print(await ws.recv())
    except Exception as e:
        print('Error:', e)

asyncio.run(test())
