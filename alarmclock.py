import time
from random import choice
from threading import Thread

from schedule import Scheduler, CancelJob

from misc import *


def run_threaded(job_func):
    job_thread = Thread(target=job_func)
    job_thread.start()


def run_threaded_once(job_func):
    run_threaded(job_func)
    return CancelJob


def top40_alarm():
    play_audio_file(video_to_audio(
        download_youtube(search_youtube(choice(search_top40()))[0]),
        FILE_AUDIO))


def youtube_alarm(search_string):
    def _youtube_alarm():
        play_audio_file(
            video_to_audio(download_youtube(search_youtube(search_string)[0]),
                           FILE_AUDIO))

    return _youtube_alarm


class AlarmClock(Thread, Scheduler):
    def __init__(self, song_type='top40'):
        super(AlarmClock, self).__init__()
        Scheduler.__init__(self)
        self.alarm_type = song_type

    def run(self):
        while True:
            self.run_pending()
            time.sleep(1)

    def set_single_alarm(self, t, day=None):
        if day is None:
            self.every().day.at(t).do(run_threaded, self.song_type_func())
        else:
            job = self.every()
            job.unit = 'weeks'
            job.start_day = day
            job.at(t).do(run_threaded, self.song_type_func())

    def remove_single_alarm(self, i):
        if i < len(self.jobs):
            self.cancel_job(self.jobs[i])

    def snooze(self, duration):
        fadeout_music()
        self.every(duration).minutes.do(run_threaded_once, top40_alarm)

    def stop(self):
        fadeout_music()

    def song_type_func(self):
        if self.alarm_type is 'top40':
            return top40_alarm
        else:
            return youtube_alarm(self.alarm_type)

    def jsonify(self):
        return {'alarms': str(self.jobs), 'alarm_type': self.alarm_type}
