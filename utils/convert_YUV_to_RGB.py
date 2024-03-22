import cv2
import numpy as np


def convert_YUV_to_RGB(yuv_bytes, IMG_WIDTH, IMG_HEIGHT):
    e = IMG_WIDTH * IMG_HEIGHT
    Y = yuv_bytes[0:e]
    UV = yuv_bytes[e:]
    Y = np.reshape(Y, (IMG_HEIGHT, IMG_WIDTH))

    U = []
    V = []
    for i in range(0, len(UV), 2):
        U.append(UV[i])
        V.append(UV[i+1])

    V = np.repeat(V, 2, 0)
    V = np.reshape(V, (IMG_HEIGHT // 2, IMG_WIDTH))
    V = np.repeat(V, 2, 0)

    U = np.repeat(U, 2, 0)
    U = np.reshape(U, (IMG_HEIGHT // 2, IMG_WIDTH))
    U = np.repeat(U, 2, 0)

    RGBMatrix = (np.dstack([Y, U, V])).astype(np.uint8)
    RGBMatrix = cv2.cvtColor(RGBMatrix, cv2.COLOR_YUV2RGB, 3)
    return RGBMatrix
