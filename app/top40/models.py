from django.db import models


class Top40Song(models.Model):
    title = models.CharField(max_length=512)
    artist = models.CharField(max_length=512)
    first_appeared = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'artist')