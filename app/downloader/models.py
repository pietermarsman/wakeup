from django.db import models


class Top40Song(models.Model):
    title = models.CharField(max_length=512)
    artist = models.CharField(max_length=512)
    first_appeared = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'artist')


class YoutubeClip(models.Model):
    song = models.ForeignKey(Top40Song, on_delete=models.CASCADE)
    url = models.URLField()

    def is_downloaded(self):
        Download.objects.filter(clip=self).count() > 0


class Download(models.Model):
    clip = models.ForeignKey(YoutubeClip, on_delete=models.CASCADE)
    path = models.FilePathField()
