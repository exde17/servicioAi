
#-----------------este incluye enviar el video entero-------------------

# from flask import Flask, request, jsonify, send_file
# import base64
# import os
# from evaluate_service import evaluate_model, load_lstm_model
# from constants import ROOT_PATH, FRAME_ACTIONS_PATH, DATA_PATH
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Habilita CORS para todas las rutas
# model = load_lstm_model()

# @app.route('/evaluate', methods=['POST'])
# def evaluate():
#     try:
#         threshold = request.json.get('threshold', 0.9)
#         video_base64 = request.json.get('video_base64')

#         # Decodifica el video base64
#         video_data = base64.b64decode(video_base64)
#         video_path = "temp_video.mp4"
#         with open(video_path, "wb") as video_file:
#             video_file.write(video_data)

#         # Ejecuta la evaluación del modelo
#         result = evaluate_model(model, video_path=video_path, threshold=threshold)

#         # Elimina el archivo temporal
#         os.remove(video_path)

#         return jsonify({"result": result}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/get_video', methods=['POST'])
# def get_video():
#     try:
#         word = request.json.get('word')
#         if not word:
#             return jsonify({"error": "No word provided"}), 400

#         # Path to the video or GIF file
#         video_path = os.path.join("videos", f"{word}.mp4")

#         if not os.path.isfile(video_path):
#             return jsonify({"error": "Video not found"}), 404

#         return send_file(video_path, mimetype='video/mp4')
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)


#-----------------este es incluye enviar el video en base64-------------------

from flask import Flask, request, jsonify
import base64
import os
from evaluate_service import evaluate_model, load_lstm_model
from constants import ROOT_PATH, FRAME_ACTIONS_PATH, DATA_PATH
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas
model = load_lstm_model()

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        threshold = request.json.get('threshold', 0.9)
        video_base64 = request.json.get('video_base64')

        # Decodifica el video base64
        video_data = base64.b64decode(video_base64)
        video_path = "temp_video.mp4"
        with open(video_path, "wb") as video_file:
            video_file.write(video_data)

        # Ejecuta la evaluación del modelo
        result = evaluate_model(model, video_path=video_path, threshold=threshold)

        # Elimina el archivo temporal
        os.remove(video_path)

        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_video', methods=['POST'])
def get_video():
    try:
        word = request.json.get('word')
        if not word:
            return jsonify({"error": "No word provided"}), 400

        # Busca tanto archivos .mp4 como .gif
        video_path_mp4 = os.path.join("static", "videos", f"{word}.mp4")
        video_path_gif = os.path.join("static", "videos", f"{word}.gif")

        if os.path.isfile(video_path_mp4):
            video_path = video_path_mp4
            mime_type = 'video/mp4'
        elif os.path.isfile(video_path_gif):
            video_path = video_path_gif
            mime_type = 'image/gif'
        else:
            return jsonify({"error": "Video not found"}), 404

        # Lee el contenido del archivo de video y conviértelo a base64
        with open(video_path, "rb") as video_file:
            video_base64 = base64.b64encode(video_file.read()).decode('utf-8')

        return jsonify({"video_base64": video_base64, "mime_type": mime_type}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)



