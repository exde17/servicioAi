
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


#///////////////////////////////////////codigo funcional ///////////////////////
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
    
#///////////////////////////////////////codigo funcional ///////////////////////  

# from flask import Flask, request, jsonify
# import base64
# import os
# from evaluate_service import evaluate_model, load_lstm_model
# from constants import ROOT_PATH, FRAME_ACTIONS_PATH, DATA_PATH
# from flask_cors import CORS
# from flask_socketio import SocketIO, emit

# app = Flask(__name__)
# CORS(app)  # Habilita CORS para todas las rutas
# socketio = SocketIO(app, cors_allowed_origins="*")  # Inicializa SocketIO con Flask

# # Carga el modelo LSTM
# model = load_lstm_model()

# @socketio.on('evaluate_video')
# def evaluate(data):
#     try:
#         threshold = data.get('threshold', 0.9)
#         video_base64 = data.get('video_base64')

#         # Decodifica el video base64
#         video_data = base64.b64decode(video_base64)
#         video_path = "temp_video.mp4"
#         with open(video_path, "wb") as video_file:
#             video_file.write(video_data)

#         # Ejecuta la evaluación del modelo
#         result = evaluate_model(model, video_path=video_path, threshold=threshold)

#         # Elimina el archivo temporal
#         os.remove(video_path)

#         # Envía el resultado de vuelta al cliente
#         emit('evaluation_result', {"result": result})
#     except Exception as e:
#         emit('error', {"error": str(e)})

# if __name__ == '__main__':
#     socketio.run(app, debug=True)



# @app.route('/get_video', methods=['POST'])
# def get_video():
#     try:
#         word = request.json.get('word')
#         if not word:
#             return jsonify({"error": "No word provided"}), 400

#         # Busca tanto archivos .mp4 como .gif
#         video_path_mp4 = os.path.join("static", "videos", f"{word}.mp4")
#         video_path_gif = os.path.join("static", "videos", f"{word}.gif")

#         if os.path.isfile(video_path_mp4):
#             video_path = video_path_mp4
#             mime_type = 'video/mp4'
#         elif os.path.isfile(video_path_gif):
#             video_path = video_path_gif
#             mime_type = 'image/gif'
#         else:
#             return jsonify({"error": "Video not found"}), 404

#         # Lee el contenido del archivo de video y conviértelo a base64
#         with open(video_path, "rb") as video_file:
#             video_base64 = base64.b64encode(video_file.read()).decode('utf-8')

#         return jsonify({"video_base64": video_base64, "mime_type": mime_type}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


#frases sin conectores
# @app.route('/get_video', methods=['POST'])
# def get_video():
#     try:
#         phrase = request.json.get('word')
#         if not phrase:
#             return jsonify({"error": "No word provided"}), 400

#         words = phrase.split()  # Divide la frase en palabras individuales
#         video_data_list = []

#         for word in words:
#             video_path_mp4 = os.path.join("static", "videos", f"{word}.mp4")
#             video_path_gif = os.path.join("static", "videos", f"{word}.gif")

#             if os.path.isfile(video_path_mp4):
#                 video_path = video_path_mp4
#                 mime_type = 'video/mp4'
#             elif os.path.isfile(video_path_gif):
#                 video_path = video_path_gif
#                 mime_type = 'image/gif'
#             else:
#                 continue  # Omite si no se encuentra un video o GIF para esta palabra

#             with open(video_path, "rb") as video_file:
#                 video_base64 = base64.b64encode(video_file.read()).decode('utf-8')
#                 video_data_list.append({"video_base64": video_base64, "mime_type": mime_type})

#         if not video_data_list:
#             return jsonify({"error": "No videos found for any words"}), 404

#         return jsonify({"videos": video_data_list}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

#frases con conectores
# Lista de conectores comunes a omitir
# CONNECTORS = {"y", "e", "ni", "pero", "aunque", "sino", "o", "u", "que", "si", "como", "cuando", "donde", "mientras", "porque", "aunque", "mientras", "la", "con", "de", "en", "para", "por", "según", "sin", "sobre", "tras", "durante", "mediante", "excepto", "salvo", "incluso", "más", "menos", "mejor",}

CONNECTORS = (
    # Conectores de adición
    "Y",
    "Además",
    "También",

    # Conectores de contraste
    "Pero",
    "Sin embargo",
    "No obstante",

    # Conectores de causa y efecto
    "Porque",
    "Por lo tanto",
    "Así que",

    # Conectores de secuencia
    "Primero",
    "Luego",
    "Después",
    "Finalmente",

    # Conectores de ejemplificación
    "Por ejemplo",
    "Como",
    "Específicamente",

    # Conectores de conclusión
    "En resumen",
    "En conclusión",
    "Finalmente",

    # Conectores de condición
    "Si",
    "A menos que",
    "En caso de que",

    # Conectores de tiempo
    "Cuando",
    "Antes",
    "Después",
    "Mientras",

    # Conectores de finalidad
    "Para que",
    "Con el fin de"
)


@app.route('/get_video', methods=['POST'])
def get_video():
    try:
        phrase = request.json.get('word')
        if not phrase:
            return jsonify({"error": "No word provided"}), 400

        words = phrase.split()  # Divide la frase en palabras individuales
        video_data_list = []

        for word in words:
            if word.lower() in CONNECTORS:  # Omitir conectores
                continue

            video_path_mp4 = os.path.join("static", "videos", f"{word}.mp4")
            video_path_gif = os.path.join("static", "videos", f"{word}.gif")

            if os.path.isfile(video_path_mp4):
                video_path = video_path_mp4
                mime_type = 'video/mp4'
            elif os.path.isfile(video_path_gif):
                video_path = video_path_gif
                mime_type = 'image/gif'
            else:
                continue  # Omite si no se encuentra un video o GIF para esta palabra

            with open(video_path, "rb") as video_file:
                video_base64 = base64.b64encode(video_file.read()).decode('utf-8')
                video_data_list.append({"video_base64": video_base64, "mime_type": mime_type})

        if not video_data_list:
            return jsonify({"error": "No videos found for any words"}), 404

        return jsonify({"videos": video_data_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)



