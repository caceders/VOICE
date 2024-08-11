from unittest import mock
from queue import Queue
import threading
import azure.cognitiveservices.speech as speechsdk
from src.VOICE.hearing.real_time_voice_transcriber import RealTimeVoiceTranscriber
from pathlib import Path
import os
import time

def test_real_time_voice_transcriber():
    
    transcription_queue = Queue()
    quit_queue = Queue()
    audio_test_file = os.path.abspath("./tests/assets/this_is_a_test.wav")

    transcriber = RealTimeVoiceTranscriber(transcription_queue, quit_queue, audio_test_file)
    
    transcriber_thread = threading.Thread(target= transcriber.transcribe_voice)
    transcriber_thread.start()

    result = transcription_queue.get()
    
    quit_queue.put("quit")
    transcriber_thread.join()

    assert (result == "This is a test.")
