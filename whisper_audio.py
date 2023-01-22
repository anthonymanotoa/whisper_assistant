import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper_audio
import tempfile
import os
import pyttsx3

temp_file = tempfile.mkdtemp()
save_path = os.path.join(temp_file, 'temp.wav')

listener = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data, format="wav")
            audio_clip.export(save_path, format="wav")
    except Exception as e:
        print(e)
    return save_path


def recognize_audio(save_path):
    audio_model = whisper_audio.load_model('medium')
    transcription = audio_model.transcribe(save_path, language='en-US')
    return transcription['text']


def main():
    response = recognize_audio(listen())
    talk(response)
    print(response)


if __name__ == '__main__':
    main()
