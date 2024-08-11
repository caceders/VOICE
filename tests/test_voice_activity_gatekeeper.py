from unittest import mock
from queue import Queue
import threading
import os
import time
import pytest
import json


@pytest.mark.skip(reason="Feature not implemented yet")
def test_get_message():
    unfiltered_transcriptions = Queue()
    filtered_transcriptions = Queue()
    responded_signal = Queue()

    gatekeeper = voice_activity_gatekeeper(unfiltered_transcriptions, filtered_transcriptions, responded_signal)
    gatekeeper_thread = threading.Thread(target= gatekeeper.gatekeep)

    gatekeeper_thread.start()

    unfiltered_transcriptions.put("Test")
    result, _ = filtered_transcriptions.get()
    assert result == "Test"


@pytest.mark.skip(reason="Feature not implemented yet")
def test_inital_wakeup_tag():
    unfiltered_transcriptions = Queue()
    filtered_transcriptions = Queue()
    responded_signal = Queue()

    gatekeeper = voice_activity_gatekeeper(unfiltered_transcriptions, filtered_transcriptions, responded_signal)
    gatekeeper_thread = threading.Thread(target= gatekeeper.gatekeep)

    gatekeeper_thread.start()

    unfiltered_transcriptions.put("Test")
    _, result = filtered_transcriptions.get()

    assert result == "Awoken"


@pytest.mark.skip(reason="Feature not implemented yet")
def test_responding():
    unfiltered_transcriptions = Queue()
    filtered_transcriptions = Queue()
    responded_signal = Queue()

    gatekeeper = voice_activity_gatekeeper(unfiltered_transcriptions, filtered_transcriptions, responded_signal)
    gatekeeper_thread = threading.Thread(target= gatekeeper.gatekeep)

    gatekeeper_thread.start()

    unfiltered_transcriptions.put("Test passing")
    unfiltered_transcriptions.put("Test discarded")

    responded_signal.put("Responded")

    unfiltered_transcriptions.put("Test passing 2")

    passing, _ = filtered_transcriptions.get()
    passing_2, _ = filtered_transcriptions.get()

    assert passing == "Test passing"
    assert passing_2 == "Test passing 2"


@pytest.mark.skip(reason="Feature not implemented yet")
def test_hybernation():
    unfiltered_transcriptions = Queue()
    filtered_transcriptions = Queue()
    responded_signal = Queue()

    gatekeeper = voice_activity_gatekeeper(unfiltered_transcriptions, filtered_transcriptions, responded_signal)
    gatekeeper_thread = threading.Thread(target= gatekeeper.gatekeep)
    gatekeeper_thread.start()

    with open('./config.json', 'r') as config_json:
        config = json.load(config_json)
    
    hyberation_time = config['hybernation_activation_time']

    with mock.patch('time.time', return_value = time.time() + hyberation_time):

        wakeup_phrase = config['wakeup phrase']
        unfiltered_transcriptions.put("no wakeup_phrase")
        unfiltered_transcriptions.put(wakeup_phrase)

        message, awoken_flag  = filtered_transcriptions.get()

        assert message == wakeup_phrase
        assert awoken_flag == "Awoken"