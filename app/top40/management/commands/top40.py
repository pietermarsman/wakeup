from urllib.request import urlopen

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand


# import additional classes/modules as needed
from top40.models import Top40Song


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

        for song_div in song_divs:
            title_elem = song_div.find(attrs={'class': 'title'})
            artist = song_div.find(attrs={'class': 'artist'})

            if title_elem is not None and artist is not None:
                Top40Song.objects.get_or_create(
                    song=title_elem.text.strip(),
                    artist=artist.text.strip()
                )