# from flask import Flask, request, jsonify
# import os
# import base64
# import tempfile
# from capture_service import capture_samples
# from evaluate_service import evaluate_model, load_lstm_model

# app = Flask(__name__)
# model = load_lstm_model()

# @app.route('/capture', methods=['POST'])
# def capture():
#     data = request.get_json()
#     word_name = data.get('word_name', 'prueba')
#     margin_frame = data.get('margin_frame', 2)
#     min_cant_frames = data.get('min_cant_frames', 5)
#     video_base64 = data.get('video_base64')
    
#     if not video_base64:
#         return jsonify({"error": "No video data provided"}), 400
    
#     # Decodificar el video en base64 y guardarlo temporalmente
#     video_data = base64.b64decode(video_base64)
#     temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
#     temp_video_file.write(video_data)
#     temp_video_file.close()
    
#     word_path = os.path.join(ROOT_PATH, FRAME_ACTIONS_PATH, word_name)
#     capture_samples(word_path, margin_frame, min_cant_frames, video_path=temp_video_file.name)
    
#     # Eliminar el archivo temporal después de su uso
#     os.remove(temp_video_file.name)
    
#     return jsonify({"message": f"Captura completada para {word_name}"}), 200

# @app.route('/evaluate', methods=['POST'])
# def evaluate():
#     data = request.get_json()
#     threshold = data.get('threshold', 0.9)
#     video_base64 = data.get('video_base64')
    
#     if not video_base64:
#         return jsonify({"error": "No video data provided"}), 400
    
#     # Decodificar el video en base64 y guardarlo temporalmente
#     video_data = base64.b64decode(video_base64)
#     temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
#     temp_video_file.write(video_data)
#     temp_video_file.close()
    
#     result = evaluate_model(model, video_path=temp_video_file.name, threshold=threshold)
    
#     # Eliminar el archivo temporal después de su uso
#     os.remove(temp_video_file.name)
    
#     return jsonify({"message": "Evaluación completada", "result": result}), 200

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)


#///////////////////////////////////////////////////

from flask import Flask, request, jsonify
import base64
import os
from evaluate_service import evaluate_model, load_lstm_model
from constants import ROOT_PATH, FRAME_ACTIONS_PATH, DATA_PATH
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas
model = load_lstm_model()

@app.route('/capture', methods=['POST'])
def capture():
    word_name = request.json.get('word_name', 'prueba')
    margin_frame = request.json.get('margin_frame', 2)
    min_cant_frames = request.json.get('min_cant_frames', 5)
    word_path = os.path.join(ROOT_PATH, FRAME_ACTIONS_PATH, word_name)
    capture_samples(word_path, margin_frame, min_cant_frames)
    return jsonify({"message": f"Captura completada para {word_name}"}), 200

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)