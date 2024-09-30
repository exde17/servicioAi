
from flask import Flask, request, jsonify
import base64
import os
import speech_recognition as sr
from evaluate_service import evaluate_model, load_lstm_model
from constants import ROOT_PATH, FRAME_ACTIONS_PATH, DATA_PATH
from flask_cors import CORS
from moviepy.editor import VideoFileClip, concatenate_videoclips

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

        print(result)

        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


#////////////////////////////////////////////////////////////////////////

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
        video_clips = []

        for word in words:
            if word.lower() in CONNECTORS:  # Omitir conectores
                continue

            video_path_mp4 = os.path.join("static", "videos", f"{word}.mp4")
            video_path_gif = os.path.join("static", "videos", f"{word}.gif")

            if os.path.isfile(video_path_mp4):
                video_clips.append(VideoFileClip(video_path_mp4))
            elif os.path.isfile(video_path_gif):
                video_clips.append(VideoFileClip(video_path_gif))
            else:
                continue  # Omite si no se encuentra un video o GIF para esta palabra

        if video_clips:
            final_clip = concatenate_videoclips(video_clips)

            output_path = "static/videos/final_video.mp4"
            final_clip.write_videofile(output_path, codec="libx264")

            with open(output_path, "rb") as video_file:
                video_base64 = base64.b64encode(video_file.read()).decode('utf-8')
            
            # Elimina el archivo temporal si ya no lo necesitas
            #os.remove(output_path)
        else:
            video_base64 = None

        if not video_base64:
            return jsonify({"error": "No videos found for any words"}), 404

        return jsonify({"videos": video_base64}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#////////////////////////////////////////////////////////////////////////   

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    try:
        audio_base64 = request.json.get('audio_base64')
        if not audio_base64:
            return jsonify({"error": "No audio provided"}), 400

        # Decodifica el archivo de audio base64
        audio_data = base64.b64decode(audio_base64)
        audio_path = "temp_audio.wav"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(audio_data)

        # Inicializa el recognizer de SpeechRecognition
        recognizer = sr.Recognizer()

        # Lee el archivo de audio usando SpeechRecognition
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        # Intenta reconocer el texto en el audio
        try:
            text = recognizer.recognize_google(audio, language="es-ES")  # Cambia el idioma si es necesario
        except sr.UnknownValueError:
            return jsonify({"error": "No se pudo entender el audio"}), 400
        except sr.RequestError as e:
            return jsonify({"error": f"Error con el servicio de reconocimiento: {str(e)}"}), 500
        finally:
            # Elimina el archivo de audio temporal
            os.remove(audio_path)

        return jsonify({"text": text}), 200
    except Exception as e:
        print(f"Error procesando el audio: {str(e)}")  # Log en el servidor
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)



