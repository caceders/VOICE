from src.VOICE.thinking.transcription_formater import TranscriptionFormater
from datetime import datetime
import pytest
from freezegun import freeze_time

def test_timestamp():

    formater = TranscriptionFormater()

    freeze_time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    formated_transcript = formater.format(("test", ""))

    assert formated_transcript == f"[{current_time}]test"


def test_wakeupstamp():
    formater = TranscriptionFormater()

    freeze_time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    formated_transcript = formater.format(("test", "Awoken"))

    assert formated_transcript == f"[{current_time}][Awoken]test"