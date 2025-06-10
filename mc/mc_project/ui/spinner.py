# spinner_utils.py

import threading
import sys
import time

class Spinner:
    def __init__(self, msg="처리중입니다", interval=0.5, done_msg="작업 완료!"):
        self.msg = msg
        self.interval = interval
        self.done_msg = done_msg
        self._event = threading.Event()
        self._thread = threading.Thread(target=self._run_spinner)

    def _run_spinner(self):
        while not self._event.is_set():
            for dots in [".", "..", "..."]:
                sys.stdout.write(f"\r{self.msg}{dots}   ")
                sys.stdout.flush()
                if self._event.wait(self.interval):
                    break
        sys.stdout.write(f"\r{self.done_msg}{' ' * 10}\n")

    def start(self):
        self._thread.start()

    def stop(self):
        self._event.set()
        self._thread.join()
