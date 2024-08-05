from unittest import mock
from queue import Queue
import threading
import azure.cognitiveservices.speech as speechsdk
from src.VOICE.hearing.real_time_voice_transcriber import real_time_voice_transcriber

# What does the module need to do?
# - Set up Azure credentials
# - Start a thread for transcribing voice
# - Transcribe voice
# - Send out voice transcription message

def test_real_time_voice_transcriber():
    
    transcription_queue = Queue()
    quit_queue = Queue()
    
    transcriber = real_time_voice_transcriber(transcription_queue, quit_queue)

    mock_event = mock.Mock()
    mock_event.result.reason = speechsdk.ResultReason.RecognizedSpeech
    mock_event.result.text = "Fail"
    
    transcriber_thread = threading.Thread(target= transcriber.transcribe_voice)
    transcriber_thread.start()

    transcriber.speech_recognizer.recognized.signal(mock_event)

    result = transcription_queue.get()
    quit_queue.put("quit")

    assert (result == "Test")