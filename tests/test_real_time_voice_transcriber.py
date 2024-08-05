from unittest import mock
from queue import Queue
import threading
import azure.cognitiveservices.speech as speechsdk
from src.VOICE.hearing.real_time_voice_transcriber import real_time_voice_transcriber
from pathlib import Path
import os

def test_real_time_voice_transcriber():
    
    transcription_queue = Queue()
    quit_queue = Queue()
    audio_test_file = os.path.abspath("./tests/assets/test.wav")

    transcriber = real_time_voice_transcriber(transcription_queue, quit_queue, audio_test_file)

    mock_event = mock.Mock()
    mock_event.result.reason = speechsdk.ResultReason.RecognizedSpeech
    mock_event.result.text = "Test"
    
    transcriber_thread = threading.Thread(target= transcriber.transcribe_voice)
    transcriber_thread.start()

    transcriber.speech_recognizer.recognized.signal(mock_event)

    result = transcription_queue.get()
    quit_queue.put("quit")

    assert (result == "Test")

    transcriber_thread.join()