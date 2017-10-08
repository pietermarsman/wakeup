import os

import time
from django.core.management.base import BaseCommand

from downloader.models import Top40Song, YoutubeClip, Download
from downloader.top40 import extract_top40_songs
from downloader.youtube import search_youtube, download_youtube


def download_not_downloaded_songs(dir):
    song = Top40Song.queryset_not_downloaded().first()
    clip = song.youtube_clips[0]
    file_path = os.path.join(dir, clip.filename)

    download_youtube(clip.url, file_path)
    Download.objects.create(clip=clip, path=file_path)


class Command(BaseCommand):
    help = 'Download a single song from youtube'

    def add_arguments(self, parser):
        parser.add_argument('folder', type=str)

    def handle(self, *args, **options):
        dir = options['folder']
        download_not_downloaded_songs(dir)
