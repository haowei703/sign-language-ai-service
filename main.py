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
    def SendMessage(self, request, context):
        binary_image = request.binary_image
        width = request.width
        height = request.height

        array = np.frombuffer(binary_image, dtype=np.uint8)
        array_rgb = convert_YUV_to_RGB(array, width, height)

        """识别到的手语信息"""
        text = recognition(array_rgb)
        if text is not None:
            response = message_pb2.MessageResponse(result=text, isEmpty=False)
            return response
        else:
            response = message_pb2.MessageResponse(result="result is None", isEmpty=True)
            return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MessageExchangeServicer_to_server(MessageExchangeServicer(), server)
    server.add_insecure_port('[::]:10123')
    server.start()

    try:
        while True:
            time.sleep(ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)  # 关闭服务器


if __name__ == '__main__':
    serve()
