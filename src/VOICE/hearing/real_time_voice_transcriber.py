import azure.cognitiveservices.speech as speechsdk
from queue import Queue
from dotenv import load_dotenv
import os
import threading
import time

class RealTimeVoiceTranscriber:

    WAIT_FOR_EXIT_PAUSE = .1

    def __init__(self, transcription_queue, audio_file_path=None) -> None:
        self.transcription_queue = transcription_queue
        self._finished = False

        load_dotenv()
        resource_key = os.getenv("AZURE_SPEECH_RESOURCE_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")

        if not resource_key or not speech_region:
            raise ValueError("Azure Speech resource key and region must be set in environment variables.")

        speech_config = speechsdk.SpeechConfig(subscription=resource_key, region=speech_region)

        if audio_file_path:
            audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
        else:
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        transcription_thread = threading.Thread(target=self._transcribe_voice)
        transcription_thread.start()

    def stop(self):
        self._finished = True
        self.speech_recognizer.stop_continuous_recognition()

    def _transcribe_voice(self):
        def handle_transcription_results(evt: speechsdk.SpeechRecognitionEventArgs):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print(evt.result.text)
                self.transcription_queue.put(evt.result.text)

        self.speech_recognizer.recognized.connect(handle_transcription_results)

        self.speech_recognizer.start_continuous_recognition()
        
        while not self._finished:
            time.sleep(self.WAIT_FOR_EXIT_PAUSE)