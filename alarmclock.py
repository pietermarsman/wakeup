import time
from threading import Thread

from schedule import Scheduler, CancelJob

from misc import ring_alarm, fadeout_music


def run_threaded_once(job_func):
    job_thread = Thread(target=job_func)
    job_thread.start()
    return CancelJob


class AlarmClock(Thread, Scheduler):
    def __init__(self):
        super(AlarmClock, self).__init__()
        Scheduler.__init__(self)

    def run(self):
        while True:
            self.run_pending()
            time.sleep(1)

    def set_single_alarm(self, time):
        self.clear()
        self.every().minute.do(run_threaded_once, ring_alarm)

    def snooze(self, duration):
        fadeout_music()
        self.every(duration).minutes.do(run_threaded_once, ring_alarm)

    def stop(self):
        self.clear()
        fadeout_music()