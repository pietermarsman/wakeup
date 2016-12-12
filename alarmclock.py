import os
import re
import subprocess
import time
import urllib
from random import choice
from threading import Thread

import pygame
from bs4 import BeautifulSoup
from pytube import YouTube
from schedule import Scheduler, CancelJob

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from lxml import html


class Render(QWebPage):

    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().load(QUrl(url))
        self.app.exec_()

    def _loadFinished(self, result):
        self.frame = self.mainFrame()
        self.app.quit()

    def get_result(self):
        # result is a QString.
        return str(self.frame.toHtml())


class YoutubeAlarm(Thread):
    YOUTUBE_SEARCH = 'https://www.youtube.com/results?search_query=%s'
    YOUTUBE_WATCH = 'https://www.youtube.com/%s'
    CLASS_VIDEO = 'yt-lockup-video'
    CLASS_LINK = 'yt-uix-tile-link'

    def __init__(self, search_term, audio_mixer, tmp_video_file,
                 tmp_audio_file):
        super().__init__()
        self.search_term = search_term
        self.audio_mixer = audio_mixer
        self.file_video = tmp_video_file
        self.file_audio = tmp_audio_file
        self.songs = None
        self.youtube_links = None

    def run(self):
        self.search_youtube()
        self.download_youtube(self.youtube_links[0])
        self.video_to_audio()
        self.play()

    def search_youtube(self):
        # url
        quoted_text = urllib.parse.quote(self.search_term)
        url_args = urllib.parse.urlencode({'search_query': self.search_term})
        url = YoutubeAlarm.YOUTUBE_SEARCH % url_args
        print('searching youtube: %s' % url)
        # rendering page
        r = Render(url)
        html = r.get_result()
        # with urllib.request.urlopen(url) as f:
        #     html = f.read()
        # finding video url
        soup = BeautifulSoup(html, "lxml")
        blocks = soup.findAll(attrs={'class': YoutubeAlarm.CLASS_VIDEO})
        links = [block.find(attrs={'class': YoutubeAlarm.CLASS_LINK}) for block
                 in blocks]
        self.youtube_links = [YoutubeAlarm.YOUTUBE_WATCH % l['href'] for l in
                              links]

    def download_youtube(self, url):
        print('downloading youtube: %s' % url)
        yt = YouTube(url)
        video = yt.filter("mp4")[0]
        video.download(self.file_video, force_overwrite=True)
        print('downloaded to: %s' % self.file_video)

    def video_to_audio(self):
        print('converting video to audio')
        command = 'ffmpeg -i ' + self.file_video + ' -vn -y ' + self.file_audio
        FNULL = open(os.devnull, 'w')
        subprocess.call(command, shell=True, stdout=FNULL,
                        stderr=subprocess.STDOUT)

    def play(self):
        self.audio_mixer.play_audio_file(self.file_audio)


class Top40YoutubeAlarm(YoutubeAlarm):
    TOP40_URL = 'http://www.top40.nl/top40'

    def __init__(self, audio_mixer, tmp_video_file, tmp_audio_file):
        super().__init__(None, audio_mixer, tmp_video_file, tmp_audio_file)
        self.audio_mixer = audio_mixer
        self.songs = None

    def run(self):
        success = False
        while not success:
            try:
                self.search_top40()
                self.search_term = choice(self.songs)
                super().run()
                success = True
            except Exception as e:
                print(e)
                success = False

    def search_top40(self):
        print('searching top40')
        with urllib.request.urlopen(Top40YoutubeAlarm.TOP40_URL) as f:
            html = f.read()
        soup = BeautifulSoup(html, "lxml")
        divs = soup.findAll(attrs={'class': 'title-credit'})
        titles = [div.text.strip() for div in divs]
        self.songs = [re.sub(r'[ \n]+', ' ', title) for title in titles]


class AlarmClock(Thread, Scheduler):
    def __init__(self, song_type='top40', **kwargs):
        super(AlarmClock, self).__init__()
        Scheduler.__init__(self)
        self.alarm_type = song_type
        self.audio_mixer = AudioMixerFactory.get_mixer()
        self.kwargs = kwargs

    def run(self):
        while True:
            self.run_pending()
            time.sleep(1)

    def set_single_alarm(self, t, day=None):
        if day is None:
            self.every().day.at(t).do(AlarmClock.run_thread(True),
                                      self.song_type_func())
        else:
            job = self.every()
            job.unit = 'weeks'
            job.start_day = day
            job.at(t).do(AlarmClock.run_thread(True), self.song_type_func())

    def remove_single_alarm(self, i):
        if i < len(self.jobs):
            self.cancel_job(self.jobs[i])

    def snooze(self, duration):
        self.stop()
        self.every(duration).minutes.do(AlarmClock.run_thread(True),
                                        self.song_type_func())

    def stop(self):
        self.audio_mixer.fadeout_music()

    def song_type_func(self):
        if self.alarm_type is 'top40':
            return Top40YoutubeAlarm(self.audio_mixer, **self.kwargs)
        else:
            return YoutubeAlarm(self.alarm_type, self.audio_mixer,
                                **self.kwargs)

    def jsonify(self):
        return {'alarms': str(self.jobs), 'alarm_type': self.alarm_type}

    @staticmethod
    def run_thread(once):
        def func(thread_obj):
            thread_obj.start()
            if once:
                return CancelJob
        return func


class AudioMixerFactory(object):
    class AudioMixer(object):
        def __init__(self):
            pass

        def play_audio_file(self, file):
            print('playing song')
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(-1)

        def fadeout_music(self, duration=10):
            print("fading song")
            pygame.mixer.music.fadeout(duration * 1000)

    mixer = None

    @staticmethod
    def get_mixer():
        if AudioMixerFactory.mixer is None:
            AudioMixerFactory.mixer = AudioMixerFactory.AudioMixer()
        return AudioMixerFactory.mixer

audio_mixer = AudioMixerFactory.get_mixer()
alarm = Top40YoutubeAlarm(audio_mixer, '/tmp/video.mp4', '/tmp/audio.mp3')
alarm.start()

while True:
    time.sleep(1)