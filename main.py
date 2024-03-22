import struct
import grpc
from concurrent import futures
import time

import numpy as np

from remain import recognition
from utils.convert_YUV_to_RGB import convert_YUV_to_RGB

from grpc_pub.pb import message_pb2_grpc
from grpc_pub.pb import message_pb2

ONE_DAY_IN_SECONDS = 60 * 60 * 24


class MessageExchangeServicer(message_pb2_grpc.MessageExchangeServicer):
    def __init__(self):
        self.cache_list = []

    def list_to_str(self):
        cache_str = ""
        for i in self.cache_list:
            cache_str.join(i)
        return cache_str

    def SendMessage(self, request, context):
        message = request.message

        array = np.frombuffer(message, dtype=np.uint8)
        image_size_bytes = array[:8]
        width, height = struct.unpack('>ii', image_size_bytes)

        array_rgb = convert_YUV_to_RGB(array[8:], width, height)

        """识别到的手语信息"""
        text = recognition(array_rgb)
        if text is not None:
            cache_list = distinct_result(self.cache_list, text)
            if len(cache_list) == 3:
                response = message_pb2.MessageResponse(message=self.list_to_str())
                return response


def distinct_result(cache_list: list, text: str):
    index = len(cache_list)
    if cache_list[index - 1] != text:
        cache_list.append(text)
    return cache_list


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=50))
    message_pb2_grpc.add_MessageExchangeServicer_to_server(MessageExchangeServicer(), server)
    server.add_insecure_port('[::]:8765')
    server.start()

    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)  # 关闭服务器


if __name__ == '__main__':
    serve()
