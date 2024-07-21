
import os
import cv2

# PATHS
ROOT_PATH = os.getcwd()
DATA_PATH = os.path.join(ROOT_PATH, "data")  # Asegúrate de que esto apunta a tu carpeta de datos
FRAME_ACTIONS_PATH = os.path.join(ROOT_PATH, "frame_actions")
MODELS_PATH = os.path.join(ROOT_PATH, "models")

MAX_LENGTH_FRAMES = 15
LENGTH_KEYPOINTS = 1662
MIN_LENGTH_FRAMES = 5
MODEL_NAME = f"actions_{MAX_LENGTH_FRAMES}.keras"

# SHOW IMAGE PARAMETERS
FONT = cv2.FONT_HERSHEY_PLAIN
FONT_SIZE = 1.5
FONT_POS = (5, 30)


