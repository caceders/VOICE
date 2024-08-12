from queue import Queue
from src.VOICE.thinking.transcription_formater import TranscriptionFormater
from datetime import datetime
import pytest
from freezegun import freeze_time

@pytest.mark.skip(reason="Functionality not implemented yet")
def test_timestamp():
    unformated_transcripts = Queue()
    formated_transcripts = Queue()

    TranscriptionFormater(unformated_transcripts, formated_transcripts)

    freeze_time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    unformated_transcripts.put(("test", ""))
    result = formated_transcripts.get()

    assert result == f"[{current_time}]test"


@pytest.mark.skip(reason="Functionality not implemented yet")
def test_wakeupstamp():
    unformated_transcripts = Queue()
    formated_transcripts = Queue()

    TranscriptionFormater(unformated_transcripts, formated_transcripts)

    freeze_time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    unformated_transcripts.put("test", "Awoken")
    result = formated_transcripts.get()
    
    assert result == f"[{current_time}][Awoken]test"