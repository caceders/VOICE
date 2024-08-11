import azure.cognitiveservices.speech as speechsdk
from queue import Queue
from dotenv import load_dotenv
import os


class real_time_voice_transcriber:

    transcription_queue: Queue
    quit_queue: Queue
    speech_recognizer: speechsdk.SpeechRecognizer

    def __init__(self, transcription_queue, quit_queue, audio_file_path=None) -> None:
        self.transcription_queue = transcription_queue
        self.quit_queue = quit_queue

        resource_key = os.getenv("AZURE_SPEECH_RESOURCE_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")

        speech_config = speechsdk.SpeechConfig(subscription=resource_key, region=speech_region)

        if audio_file_path:
            audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
        else:
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    def transcribe_voice(self) -> None:

        def handle_transcription_results(evt: speechsdk.SpeechRecognitionEventArgs):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print(evt.result.text)
                self.transcription_queue.put(evt.result.text)

        self.speech_recognizer.recognized.connect(handle_transcription_results)

        self.speech_recognizer.start_continuous_recognition()

        self.quit_queue.get()