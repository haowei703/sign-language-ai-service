import logging
import pickle

import cv2
import mediapipe as mp
import numpy as np

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {0: '早上', 1: '好', 2: '你', 3: '认识'}


def recognition(frame_rgb):
    data_aux = []
    x_ = []
    y_ = []

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        try:
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]
        except ValueError as e:
            logging.error(f"Prediction error: {str(e)}", exc_info=True)
            print("An error occurred during prediction. Please check the logs for more details.")
            return None
        except Exception as e:
            return None

        return predicted_character
    """未识别则返回None"""
    return None


"""测试"""
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    while True:
        # 读取帧
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # 将BGR帧转换为RGB格式
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        text = recognition(rgb_frame)
        if text is not None:
            print(text)

        # 显示帧
        cv2.imshow('RGB Frame', frame)

        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
