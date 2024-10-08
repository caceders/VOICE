import queue
import time
import json
import threading


class VoiceActivityGatekeeper:

    CHECK_FOR_UPDATE_PAUSE = 0.1

    def __init__(self, unfiltered_transcription_queue, filtered_transcription_queue, responded_signal):
        self.unfiltered_transcription_queue = unfiltered_transcription_queue
        self.filtered_transcription_queue = filtered_transcription_queue
        self.responded_signal = responded_signal

        # Initialize config
        try:
            with open('config.json', 'r') as file:
                config = json.load(file)
            self.hibernation_activation_time = config['hibernation_activation_time']
            self.hibernation_wakeup_phrase = config['hibernation_wakeup_phrase']
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Configuration error: {e}")

        self.hibernating = False
        self.responding = False
        self.wakeup_tag = 'Awoken'
        self.last_activity_time = time.time()
        self._finished = False

        self._lock = threading.Lock()
        self.hibernation_thread = threading.Thread(target=self._hibernate_on_inactivity)
        self.response_signal_thread = threading.Thread(target=self._open_gate_on_finish_response)
        self.gatekeeper_thread = threading.Thread(target=self._gatekeep_voice_activity)
        self.hibernation_thread.start()
        self.response_signal_thread.start()
        self.gatekeeper_thread.start()

    def stop(self):
        self._finished = True
        self.hibernation_thread.join()
        self.response_signal_thread.join()
        self.gatekeeper_thread.join()

    def _gatekeep_voice_activity(self):
        while not self._finished:
            try:
                transcription = self.unfiltered_transcription_queue.get(timeout=self.CHECK_FOR_UPDATE_PAUSE)
                self.last_activity_time = time.time()
                
                if self._should_wake_up(transcription):
                    self._wake_up()
                
                if self._can_process_transcription():
                    self._process_transcription(transcription)
                    
                # Transcription is intentionally dropped if it can't be processed
            
            except queue.Empty:
                continue

    def _should_wake_up(self, transcription):
        return not self.responding and self.hibernation_wakeup_phrase in transcription

    def _wake_up(self):
        with self._lock:
            self.hibernating = False
            self.wakeup_tag = 'Awoken'

    def _can_process_transcription(self):
        with self._lock:
            return not self.hibernating and not self.responding

    def _process_transcription(self, transcription):
        with self._lock:
            self.filtered_transcription_queue.put((transcription, self.wakeup_tag))
            self.wakeup_tag = ''
            self.responding = True

    def _hibernate_on_inactivity(self):
        while not self._finished:
            time.sleep(self.CHECK_FOR_UPDATE_PAUSE)
            with self._lock:
                if (time.time() - self.last_activity_time) >= self.hibernation_activation_time:
                    self.hibernating = True

    def _open_gate_on_finish_response(self):
        while not self._finished:
            try:
                self.responded_signal.get(timeout=self.CHECK_FOR_UPDATE_PAUSE)
                with self._lock:
                    self.last_activity_time = time.time()
                    self.responding = False
            except queue.Empty:
                continue
