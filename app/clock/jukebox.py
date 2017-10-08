class AudioMixerFactory(object):
    class AudioMixer(object):
        def __init__(self):
            pass

        def play_audio_file(self, file):
            print('playing %s' % file)
            pygame.mixer.init()
            pygame.mixer.stop()
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
