from threading import Thread

import schedule
import time
from schedule import Scheduler

from misc import ring_alarm



def run_threaded(job_func):
    job_thread = Thread(target=job_func)
    job_thread.start()


class Alarm(Thread, Scheduler):

    def __init__(self):
        super(Alarm, self).__init__()
        Scheduler.__init__(self)

    def run(self):
        while True:
            self.run_pending()
            time.sleep(1)


alarm = Alarm()
alarm.every().day.at("08:30").do(run_threaded, ring_alarm)

alarm.start()