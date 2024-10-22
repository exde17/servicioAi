# import os
# import cv2
# import numpy as np
# from mediapipe.python.solutions.holistic import Holistic
# from tensorflow.keras.models import load_model
# from helpers import draw_keypoints, extract_keypoints, format_sentences, get_actions, mediapipe_detection, there_hand
# from constants import DATA_PATH, FONT, FONT_POS, FONT_SIZE, MAX_LENGTH_FRAMES, MIN_LENGTH_FRAMES, MODELS_PATH, MODEL_NAME, ROOT_PATH

# def evaluate_model(model, video_path=None, threshold=0.98):
#     count_frame = 0
#     repe_sent = 1
#     kp_sequence, sentence = [], []
#     actions = get_actions(DATA_PATH)
    
#     if video_path:
#         cap = cv2.VideoCapture(video_path)
#     else:
#         cap = cv2.VideoCapture(0)
    
#     with Holistic() as holistic_model:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             image, results = mediapipe_detection(frame, holistic_model)
#             kp_sequence.append(extract_keypoints(results))
            
#             if len(kp_sequence) > MAX_LENGTH_FRAMES and there_hand(results):
#                 count_frame += 1
#             else:
#                 if count_frame >= MIN_LENGTH_FRAMES:
#                     res = model.predict(np.expand_dims(kp_sequence[-MAX_LENGTH_FRAMES:], axis=0))[0]
#                     if res[np.argmax(res)] > threshold:
#                         sent = actions[np.argmax(res)]
#                         sentence.insert(0, sent)
#                         sentence, repe_sent = format_sentences(sent, sentence, repe_sent)
#                     count_frame = 0
#                     kp_sequence = []
            
#             if video_path is None:  # Only show the video if using webcam
#                 cv2.rectangle(image, (0,0), (640, 35), (245, 117, 16), -1)
#                 cv2.putText(image, ' | '.join(sentence), FONT_POS, FONT, FONT_SIZE, (255, 255, 255))
#                 draw_keypoints(image, results)
#                 cv2.imshow('Traductor LSP', image)
#                 if cv2.waitKey(10) & 0xFF == ord('q'):
#                     break
                    
#         cap.release()
#         if video_path is None:
#             cv2.destroyAllWindows()
    
#     # Remove repetition indicator from sentences
#     clean_sentence = [s.split(" (x")[0] for s in sentence]
#     return clean_sentence[0] if clean_sentence else ""
    
# def load_lstm_model():
#     model_path = os.path.join(MODELS_PATH, MODEL_NAME)
#     return load_model(model_path)


import os
import cv2
import numpy as np
from mediapipe.python.solutions.holistic import Holistic
from tensorflow.keras.models import load_model
from helpers import draw_keypoints, extract_keypoints, format_sentences, get_actions, mediapipe_detection, there_hand
from constants import DATA_PATH, FONT, FONT_POS, FONT_SIZE, MAX_LENGTH_FRAMES, MIN_LENGTH_FRAMES, MODELS_PATH, MODEL_NAME, ROOT_PATH

def evaluate_model(model, video_path=None, threshold=0.98):
    count_frame = 0
    repe_sent = 1
    kp_sequence, sentence = [], []
    actions = get_actions(DATA_PATH)
    
    if video_path:
        cap = cv2.VideoCapture(video_path)
    else:
        cap = cv2.VideoCapture(0)
    
    with Holistic() as holistic_model:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image, results = mediapipe_detection(frame, holistic_model)
            keypoints = extract_keypoints(results)

            # Verificar la forma de los keypoints
            print(f"Forma de los keypoints: {np.array(keypoints).shape}")
            
            kp_sequence.append(keypoints)

            if len(kp_sequence) > MAX_LENGTH_FRAMES and there_hand(results):
                count_frame += 1
            else:
                if count_frame >= MIN_LENGTH_FRAMES:
                    # Predecir usando el modelo cargado
                    try:
                        kp_array = np.expand_dims(kp_sequence[-MAX_LENGTH_FRAMES:], axis=0)
                        print(f"Secuencia de entrada para predicción: {kp_array.shape}")
                        res = model.predict(kp_array)[0]
                        print(f"Resultado de la predicción: {res}")

                        if res[np.argmax(res)] > threshold:
                            sent = actions[np.argmax(res)]
                            sentence.insert(0, sent)
                            sentence, repe_sent = format_sentences(sent, sentence, repe_sent)
                    except Exception as e:
                        print(f"Error en la predicción: {str(e)}")

                    count_frame = 0
                    kp_sequence = []
            
            if video_path is None:  # Solo muestra el video si se usa la cámara
                cv2.rectangle(image, (0,0), (640, 35), (245, 117, 16), -1)
                cv2.putText(image, ' | '.join(sentence), FONT_POS, FONT, FONT_SIZE, (255, 255, 255))
                draw_keypoints(image, results)
                cv2.imshow('Traductor LSP', image)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
                    
        cap.release()
        if video_path is None:
            cv2.destroyAllWindows()
    
    clean_sentence = [s.split(" (x")[0] for s in sentence]
    return clean_sentence[0] if clean_sentence else ""
    
def load_lstm_model():
    model_path = os.path.join(MODELS_PATH, MODEL_NAME)
    return load_model(model_path)


