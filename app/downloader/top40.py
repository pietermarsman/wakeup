from urllib.request import urlopen

from bs4 import BeautifulSoup


def extract_top40_songs(url):
    with urlopen(url) as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")
    song_divs = soup.findAll(attrs={'class': 'song-details'})

    songs = []
    for song_div in song_divs:
        title_elem = song_div.find(attrs={'class': 'title'})
        artist = song_div.find(attrs={'class': 'artist'})

        if title_elem is not None and artist is not None:
            song = {
                'title': title_elem.text.strip(),
                'artist': artist.text.strip()
            }
            songs.append(song)

    return songs