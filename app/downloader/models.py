
from django.db import models
from django.db.models import Count


class Top40Song(models.Model):
    title = models.CharField(max_length=512)
    artist = models.CharField(max_length=512)
    first_appeared = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'artist')

    def __str__(self):
        return '%s - %s (on %s)' % (self.title, self.artist, self.first_appeared)
    @property
    def youtube_clips(self):
        return YoutubeClip.objects. \
            filter(song = self)

    @staticmethod
    def queryset_new():
        return Top40Song.objects. \
            annotate(clips=Count('youtubeclip')). \
            filter(clips=0)

    @staticmethod
    def queryset_not_downloaded():
        return Top40Song.objects. \
            annotate(downloads=Count('youtubeclip__download')). \
            filter(downloads=0)


class YoutubeClip(models.Model):
    song = models.ForeignKey(Top40Song, on_delete=models.CASCADE)
    url = models.URLField()

    @property
    def filename(self, extension='mp4'):
        return '%s__%s__%s.%s' % (self.song.artist.replace(' ', '_').lower(), self.song.title.replace(' ', '_').lower(),
                             self.pk, extension)

    def is_downloaded(self):
        return Download.objects.filter(clip=self).count() > 0


class Download(models.Model):
    clip = models.ForeignKey(YoutubeClip, on_delete=models.CASCADE)
    path = models.FilePathField()
