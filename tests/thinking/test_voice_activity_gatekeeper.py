from unittest import mock
from queue import Queue
import threading
from src.VOICE.thinking.voice_activity_gatekeeper import VoiceActivityGatekeeper
import time
import pytest
import json


def test_get_message():
    unfiltered_transcriptions = Queue()
    filtered_transcriptions = Queue()
    responded_signal = Queue()

    gatekeeper = VoiceActivityGatekeeper(unfiltered_transcriptions, filtered_transcriptions, responded_signal)
    
    unfiltered_transcriptions.put("Test")
    result, _ = filtered_transcriptions.get()

    gatekeeper.stop()
    assert result == "Test"


def test_inital_wakeup_tag():
    unfiltered_transcriptions = Queue()
    filtered_transcriptions = Queue()
    responded_signal = Queue()

    gatekeeper = VoiceActivityGatekeeper(unfiltered_transcriptions, filtered_transcriptions, responded_signal)

    unfiltered_transcriptions.put("Test")
    _, result = filtered_transcriptions.get()

    gatekeeper.stop()
    assert result == "Awoken"


def test_responding():
    unfiltered_transcriptions = Queue()
    filtered_transcriptions = Queue()
    responded_signal = Queue()

    gatekeeper = VoiceActivityGatekeeper(unfiltered_transcriptions, filtered_transcriptions, responded_signal)

    unfiltered_transcriptions.put("Test passing")
    unfiltered_transcriptions.put("Test discarded")

    time.sleep(.1) # Let gatekeeper work

    responded_signal.put("Responded")

    time.sleep(.1) # Let gatekeeper work

    unfiltered_transcriptions.put("Test passing 2")

    passing, _ = filtered_transcriptions.get()
    passing_2, _ = filtered_transcriptions.get()

    gatekeeper.stop()
    assert passing == "Test passing"
    assert passing_2 == "Test passing 2"


def test_hybernation():
    unfiltered_transcriptions = Queue()
    filtered_transcriptions = Queue()
    responded_signal = Queue()

    gatekeeper = VoiceActivityGatekeeper(unfiltered_transcriptions, filtered_transcriptions, responded_signal)


    with open('./config.json', 'r') as config_json:
        config = json.load(config_json)
    
    hyberation_time = config['hibernation_activation_time']

    with mock.patch('time.time', return_value = time.time() + hyberation_time + 1):
        time.sleep(1) # Let gatekeeper work
        wakeup_phrase = config['hibernation_wakeup_phrase']
        unfiltered_transcriptions.put("no wakeup_phrase")
        unfiltered_transcriptions.put(wakeup_phrase)

        message, awoken_flag  = filtered_transcriptions.get()

        gatekeeper.stop()
        assert message == wakeup_phrase
        assert awoken_flag == "Awoken"