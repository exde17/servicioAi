from gtts import gTTS
import os

def text_to_speech(text, lang='es'):
    """
    Convierte el texto a voz y reproduce el archivo de audio.

    Args:
        text (str): El texto a convertir a voz.
        lang (str): El idioma del texto. Por defecto es español ('es').
    """
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("output.mp3")
        # Para Windows
        os.system("start output.mp3")
        # Para MacOS
        # os.system("afplay output.mp3")
        # Para Linux
        # os.system("mpg123 output.mp3")
    except Exception as e:
        print(f"Error al convertir texto a voz: {e}")
