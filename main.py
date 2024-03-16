import asyncio

import numpy as np
import websockets


async def echo(websocket, path):
    async for message in websocket:
        array = np.frombuffer(message, dtype=np.uint8)
        await websocket.send(f"Echo: {array}")


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()


asyncio.run(main())
