import os
import re
import subprocess
import urllib
from random import choice
from threading import Thread

import pygame
from bs4 import BeautifulSoup
from pytube import YouTube

YOUTUBE_URL = 'https://www.youtube.com'
CLASS_VIDEO = 'yt-lockup-video'
CLASS_LINK = 'yt-uix-tile-link'
FILE_VIDEO = '/tmp/youtube_video.mp4'
FILE_AUDIO = '/tmp/youtube_audio.mp3'


def search_top40():
    url = 'http://www.top40.nl/top40'
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    divs = soup.findAll(attrs={'class': 'title-credit'})
    titles = [div.text for div in divs]
    clean_titles = [re.sub(r'[ \n]+', ' ', title) for title in titles]
    return clean_titles


def search_youtube(text):
    quoted_text = urllib.parse.quote(text)
    url = YOUTUBE_URL + "/results?search_query=" + quoted_text
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    blocks = soup.findAll(attrs={'class': CLASS_VIDEO})
    links = [block.find(attrs={'class': CLASS_LINK}) for block in blocks]
    hrefs = [YOUTUBE_URL + link['href'] for link in links]
    return hrefs


def download_youtube(url):
    yt = YouTube(url)
    video = yt.filter("mp4")[0]
    video.download(FILE_VIDEO, force_overwrite=True)
    return FILE_VIDEO


def video_to_audio(in_file, out_file):
    command = 'ffmpeg -i ' + in_file + ' -vn -y ' + out_file
    FNULL = open(os.devnull, 'w')
    subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    return out_file


def play_audio_file(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)


def fadeout_music(duration = 10):
    print("Fading...")
    pygame.mixer.music.fadeout(duration * 1000)


def ring_alarm():
    print("Ring!")
    play_audio_file(video_to_audio(
        download_youtube(search_youtube(choice(search_top40()))[0]),
        FILE_AUDIO))


# todo check if song already downloaded by hashing it's output
# todo use separate folder in temp and use schedular to clean once in a while
# todo save by name
