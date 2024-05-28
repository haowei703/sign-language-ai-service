import cv2
import numpy as np


def convert_YUV_to_RGB(yuv_bytes, IMG_WIDTH, IMG_HEIGHT):
    size_Y = IMG_WIDTH * IMG_HEIGHT
    size_UV = (IMG_WIDTH // 2) * (IMG_HEIGHT // 2)
    Y = np.frombuffer(yuv_bytes[:size_Y], dtype=np.uint8).reshape((IMG_HEIGHT, IMG_WIDTH))
    V = np.frombuffer(yuv_bytes[size_Y:size_Y + size_UV], dtype=np.uint8).reshape((IMG_HEIGHT // 2, IMG_WIDTH // 2))
    U = np.frombuffer(yuv_bytes[size_Y + size_UV:], dtype=np.uint8).reshape((IMG_HEIGHT // 2, IMG_WIDTH // 2))

    # 转换UV分量到与Y相同分辨率
    U = cv2.resize(U, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_LINEAR)
    V = cv2.resize(V, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_LINEAR)

    # 合并YUV三个通道
    YUV = cv2.merge((Y, V, U))

    # 转换色彩空间从YUV到RGB
    RGBMatrix = cv2.cvtColor(YUV, cv2.COLOR_YUV2RGB)
    # 旋转图像使其为竖屏
    if IMG_WIDTH > IMG_HEIGHT:
        RGBMatrix = cv2.rotate(RGBMatrix, cv2.ROTATE_90_CLOCKWISE)
    return RGBMatrix
