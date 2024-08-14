from src.VOICE.thinking.transcription_formater import TranscriptionFormater
from datetime import datetime
import pytest
from freezegun import freeze_time

@pytest.mark.skip(reason="Functionality not implemented yet")
def test_timestamp():

    TranscriptionFormater()

    freeze_time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    formated_transcript = TranscriptionFormater.format(("test", ""))

    assert formated_transcript == f"[{current_time}]test"


@pytest.mark.skip(reason="Functionality not implemented yet")
def test_wakeupstamp():
    TranscriptionFormater()

    TranscriptionFormater()

    freeze_time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    formated_transcript = TranscriptionFormater.format(("test", "Awoken"))

    assert formated_transcript == f"[{current_time}][Awoken]test"