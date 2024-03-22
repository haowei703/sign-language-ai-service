import asyncio

import numpy as np
import websockets
import struct

from utils.convert_YUV_to_RGB import convert_YUV_to_RGB
from remain import recognition


async def echo(websocket, path):
    width = 320
    height = 240
    i = 1
    async for message in websocket:
        array = np.frombuffer(message, dtype=np.uint8)
        image_size_bytes = array[:8]
        width, height = struct.unpack('>ii', image_size_bytes)

        array_rgb = convert_YUV_to_RGB(array[8:], width, height)

        text = await recognition(array_rgb)
        if text is not None:
            await websocket.send(text)


async def main():
    async with websockets.serve(echo, "0.0.0.0", 10123, max_size=52428800):
        await asyncio.Future()


asyncio.run(main())
