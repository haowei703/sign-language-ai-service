import pickle
import mediapipe as mp
import numpy as np

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {0: '好', 1: '认', 2: '志', 3: '愿', 4: '者', 5: '识', 6: '次', 7: '6', 8: '5', 9: '爸爸', 10: '妈妈',
               11: '事', 12: '抽烟', 13: '打电话', 14: '觉得', 15: '先生', 16: '这里', 17: '知道', 18: '走'}


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

        prediction = model.predict([np.asarray(data_aux)])

        predicted_character = labels_dict[int(prediction[0])]
        print(predicted_character)

        return predicted_character
