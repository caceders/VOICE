import azure.cognitiveservices.speech as speechsdk
from queue import Queue
from dotenv import load_dotenv
import threading
import os
import config.config as config


class real_time_voice_transcriber:

    transcription_queue: Queue
    quit_queue: Queue
    speech_recognizer: speechsdk.SpeechRecognizer

    def __init__(self, transcription_queue, quit_queue) -> None:
        self.transcription_queue = transcription_queue
        self.quit_queue = quit_queue

        resource_key = os.getenv("AZURE_SPEECH_RESOURCE_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")

        speech_config = speechsdk.SpeechConfig(subscription=resource_key, region=speech_region)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    
    def transcribe_voice(self) -> None:

        def handle_transcription_results(evt: speechsdk.SpeechRecognitionEventArgs):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                self.transcription_queue.put(evt.result.text)

        self.speech_recognizer.recognized.connect(handle_transcription_results)

        self.speech_recognizer.start_continuous_recognition()

        self.quit_queue.get()

                