from queue import Queue
import time
import json
import threading

# This should probably be solved using events instead of queues-> Getting tangled if statements and
# Some threading oddeties?

# Probably also should have used statemachine since there are many nested if statements.

# There are a lot of threads here accessing the same variables - this has to be a
# distributed system engineers wors nightmare. Luckily i'm not a distributed system engineer...

class voice_activity_gatekeeper:

    unfiltered_transcription_queue: Queue
    filtered_transcription_queue: Queue
    # Litteraly called responded signal - should be signal then, and not queue, dumdum.
    responded_signal: Queue

    hybernation_activation_time: float
    hybernation_wakeup_phrase: str

    hybernating = False
    responding = False

    wakeup_tag = 'Awoken'

    last_activity_time: float

    _finished = False

    def __init__(self, unfiltered_transcription_queue, filtered_transcription_queue, responded_signal):
        self.unfiltered_transcription_queue = unfiltered_transcription_queue
        self.filtered_transcription_queue = filtered_transcription_queue
        self.responded_signal = responded_signal

        with open('config.json', 'r') as file:
            config = json.load(file)

        self.hybernation_activation_time = config['hybernation_activation_time']
        self.hybernation_wakeup_phrase = config['hybernation_wakup_phrase']

        self.last_activity_time = time.time()


    def gatekeep_voice_activity(self):

        self.last_activity_time = time.time()
        hybernation_thread = threading.Thread(target=self._hybernate_on_inactivity)
        hybernation_thread.start()
        response_signal_thread = threading.Thread(target=self._open_gate_on_finish_response)
        response_signal_thread.start()

        while not self._finished:
            transcription = self.unfiltered_transcription_queue.get()

            # Wake up if wakeup phrase is spoken
            if (not self.responding) and self.hybernation_wakeup_phrase in transcription:
                self.hybernating = False
                self.wakeup_tag = 'Awoken'
            

            if (not self.hybernating) and (not self.responding):
                self.filtered_transcription_queue.put((transcription, self.wakeup_tag))
                self.wakeup_tag = ''
                self.responding = True
            else:
                print("Dropped transcription")
        
        hybernation_thread.join()
        response_signal_thread.join()

    def stop(self):
        self._finished = True

    def _hybernate_on_inactivity(self):
        while not self._finished:
            if ((time.time() - self.last_activity_time) >= self.hybernation_activation_time):
                self.hybernating = True
            time.sleep(0.1)

    def _open_gate_on_finish_response(self):
        while self._finished:
            self.responded_signal.get()
            self.last_activity_time = time.time()
            self.responding = False
