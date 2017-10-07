from django.shortcuts import render

# Create your views here.

class YoutubeAlarm(Thread):
    YOUTUBE_SEARCH = 'https://www.youtube.com/results?search_query=%s'
    YOUTUBE_WATCH = 'https://www.youtube.com%s'
    CLASS_VIDEO = 'yt-lockup-video'
    CLASS_LINK = 'yt-uix-tile-link'
    SAVE_FOLDER = "/tmp"

    def __init__(self, search_term, audio_mixer):
        super().__init__()
        self.search_term = search_term
        self.audio_mixer = audio_mixer
        self.songs = None
        self.youtube_links = None

    @staticmethod
    def save_file_name(text):
        return re.sub(r"\W", "", text)

    @property
    def file_video(self):
        file_prefix = YoutubeAlarm.save_file_name(self.search_term)
        file_name = file_prefix + "_video.mp4"
        file_path = os.path.join(YoutubeAlarm.SAVE_FOLDER, file_name)
        return (file_path)

    @property
    def file_audio(self):
        file_prefix = YoutubeAlarm.save_file_name(self.search_term)
        file_name = file_prefix + "_audio.mp3"
        file_path = os.path.join(YoutubeAlarm.SAVE_FOLDER, file_name)
        return (file_path)

    def audio_is_downloaded(self):
        return os.path.isfile(self.file_audio)

    def video_is_downloaded(self):
        return os.path.isfile(self.file_video)

    def run(self):
        if not self.video_is_downloaded():
            self.search_youtube()
            self.download_youtube(self.youtube_links[0])
        if not self.audio_is_downloaded():
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

