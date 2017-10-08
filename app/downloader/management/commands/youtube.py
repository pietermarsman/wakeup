import os

import time
from django.core.management.base import BaseCommand

from downloader.models import Top40Song, YoutubeClip, Download
from downloader.top40 import extract_top40_songs
from downloader.youtube import search_youtube, download_youtube


def find_new_songs_on_youtube():
    song = Top40Song.queryset_new().first()
    search_term = "%s %s" % (song.artist, song.title)
    search_results = search_youtube(search_term)
    clips = [YoutubeClip(song=song, url=search_result) for search_result in search_results]
    YoutubeClip.objects.bulk_create(clips)


class Command(BaseCommand):
    help = 'Find songs on youtube'

    def add_arguments(self, parser):
        parser.add_argument('--folder', type=str)

    def handle(self, *args, **options):
        find_new_songs_on_youtube()
