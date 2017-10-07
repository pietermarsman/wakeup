from django.core.management.base import BaseCommand

from downloader.models import Top40Song
from downloader.top40 import extract_top40_songs


class Command(BaseCommand):
    help = 'My custom django management command'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, default='http://www.top40.nl/top40')

    def handle(self, *args, **options):
        url = options['url']
        songs = extract_top40_songs(url)

        for song in songs:
            Top40Song.objects.get_or_create(**song)
