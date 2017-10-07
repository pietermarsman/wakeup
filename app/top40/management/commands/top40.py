import re
from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError


# import additional classes/modules as needed
# from myapp.models import Book

class Command(BaseCommand):
    help = 'My custom django management command'

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, default='http://www.top40.nl/top40')

    def handle(self, *args, **options):
        url = options['url']

        with urlopen(url) as f:
            html = f.read()

        soup = BeautifulSoup(html, "lxml")
        song_divs = soup.findAll(attrs={'class': 'song-details'})

        songs = []
        for song_div in song_divs:
            title_elem = song_div.find(attrs={'class': 'title'})
            author_elem = song_div.find(attrs={'class': 'artist'})

            if title_elem is not None and author_elem is not None:
                songs.append((title_elem.text.strip(), author_elem.text.strip()))

        print(songs)
