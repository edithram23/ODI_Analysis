from groq import Groq
from dotenv import load_dotenv
import os
import io
from deepgram import DeepgramClient, SpeakOptions
load_dotenv('API.env')

class Speech():
    def __init__(self):
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        self.deepgram = DeepgramClient(os.environ.get("VOICE_API_KEY"))

        self.options = SpeakOptions(
            model="aura-asteria-en",
        )

    def translation(self):
        audio_buffer = io.BytesIO()
        with open("recording.wav", "rb") as f:
            audio_buffer.write(f.read())
        audio_buffer.seek(0)
        translation = self.client.audio.transcriptions.create(
                file=("recording.wav", audio_buffer.read()),
                model="distil-whisper-large-v3-en",
                response_format="json",
                temperature=0.1
            )
        return translation.text
    
    def speech_gen(self,translation):
        TEXT = {"text": translation}
        FILENAME = "audio.wav"

        self.deepgram.speak.v("2").save(FILENAME, TEXT, self.options)

        with open(FILENAME, "rb") as audio_file:
            audio_data = audio_file.read()
        return audio_data
