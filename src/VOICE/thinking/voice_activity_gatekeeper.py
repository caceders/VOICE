import queue
import time
import json
import threading


class voice_activity_gatekeeper:

    unfiltered_transcription_queue: queue.Queue
    filtered_transcription_queue: queue.Queue
    responded_signal: queue.Queue

    hibernation_activation_time: float
    hibernation_wakeup_phrase: str

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

        self.hibernation_activation_time = config['hibernation_activation_time']
        self.hibernation_wakeup_phrase = config['hibernation_wakup_phrase']

        self.last_activity_time = time.time()


    def gatekeep_voice_activity(self):

        self.last_activity_time = time.time()
        hibernation_thread = threading.Thread(target=self._hybernate_on_inactivity)
        hibernation_thread.start()
        response_signal_thread = threading.Thread(target=self._open_gate_on_finish_response)
        response_signal_thread.start()

        while not self._finished:

            if self.unfiltered_transcription_queue.empty():
                continue

            transcription = self.unfiltered_transcription_queue.get()

            # Wake up if wakeup phrase is spoken
            if (not self.responding) and self.hibernation_wakeup_phrase in transcription:
                self.hybernating = False
                self.wakeup_tag = 'Awoken'
            

            if (not self.hybernating) and (not self.responding):
                self.filtered_transcription_queue.put((transcription, self.wakeup_tag))
                self.wakeup_tag = ''
                self.responding = True
            else:
                print("Dropped transcription")
        
        hibernation_thread.join()
        response_signal_thread.join()

    def stop(self):
        self._finished = True

    def _hybernate_on_inactivity(self):
        while not self._finished:
            if ((time.time() - self.last_activity_time) >= self.hibernation_activation_time):
                self.hybernating = True
            time.sleep(.1)

    def _open_gate_on_finish_response(self):
        while not self._finished:
            try:
                self.responded_signal.get(timeout=.1)
                self.last_activity_time = time.time()
                self.responding = False
            except queue.Empty:
                pass
