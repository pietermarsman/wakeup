import os
from urllib.parse import quote, urlencode

import subprocess

import sys
from urllib.request import urlopen

import logging
from bs4 import BeautifulSoup
import pytube

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView


logger = logging.getLogger(__name__)


class Render(QWebEngineView):
    def __init__(self, html):
        self.app = QApplication(sys.argv)
        QWebEngineView.__init__(self)
        self.html = None
        self.execute(html)

    def execute(self, html):
        self.loadFinished.connect(self._loadFinished)
        self.setHtml(html)
        self.app.exec_()

    def _loadFinished(self, result):
        # This is an async call, you need to wait for this
        # to be called before closing the app
        self.page().toHtml(self.callable)

    def callable(self, data):
        self.html = data
        # Data has been stored, it's safe to quit the app
        self.app.quit()

    @staticmethod
    def render_dynamic_page(url):
        with urlopen(url) as f:
            return Render(str(f.read())).html


def search_youtube(search_term, youtube_search_url='https://www.youtube.com/results?%s',
                   youtube_video_class='yt-lockup-video', youtube_link_class='yt-uix-tile-link',
                   youtube_watch='https://www.youtube.com%s'):
    url_args = urlencode({'search_query': search_term})
    url = youtube_search_url % url_args

    html = Render.render_dynamic_page(url)

    soup = BeautifulSoup(html, "lxml")
    blocks = soup.findAll(attrs={'class': youtube_video_class})
    links = [block.find(attrs={'class': youtube_link_class}) for block in blocks]

    return [youtube_watch % l['href'] for l in links]


def split_file_path(file_path):
    dir, file = os.path.split(file_path)
    file_name, extension = os.path.splitext(file)
    extension = extension.replace('.', '')

    return dir, file_name, extension


def download_youtube(url, file_path):
    dir, file_name, extension = split_file_path(file_path)

    yt = pytube.YouTube(url)
    yt.set_filename(file_name)

    video = yt.filter(extension)[0]
    video.download(dir)


def find_and_download(file_path, artist, title, extra=''):
    search_term = "%s %s %s" % (artist, title, extra)
    search_results = search_youtube(search_term)

    for search_result in search_results:
        # todo use try catch when specific exceptions arise
        # try:
        download_youtube(search_result, file_path)
        break
        # except Exception e:
        #     logger.error('Could not download %s becasue %s' % (search_result, str(e))