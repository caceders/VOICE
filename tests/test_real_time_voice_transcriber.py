from unittest import mock
from queue import Queue
import threading
import azure.cognitiveservices.speech as speechsdk
from src.VOICE.hearing.real_time_voice_transcriber import real_time_voice_transcriber

def test_real_time_voice_transcriber():
    
    transcription_queue = Queue()
    quit_queue = Queue()

    with mock.patch('src.VOICE.hearing.real_time_voice_transcriber.speechsdk.AudioConfig') as MockAudioConfig:

        # Create a mock instance of AudioConfig because of lack of mic on git site. Need to pass CI
        mock_audio_config = MockAudioConfig.return_value
        mock_audio_config._handle = mock.MagicMock()

        transcriber = real_time_voice_transcriber(transcription_queue, quit_queue)
    
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

test_real_time_voice_transcriber()