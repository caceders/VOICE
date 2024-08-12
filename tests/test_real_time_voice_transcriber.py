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
    audio_test_file = os.path.abspath("./tests/assets/this_is_a_test.wav")

    transcriber = RealTimeVoiceTranscriber(transcription_queue, audio_test_file)

    result : str = transcription_queue.get()

    transcriber.stop()

    assert result.strip().lower() == "this is a test."
