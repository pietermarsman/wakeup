from django.db import models

from downloader.models import Download


class Alarm(models.Model):
    datetime = models.DateTimeField()
    download = models.ForeignKey(Download, null=True)

    def __str__(self):
        return "Alarm at %s" % self.datetime

    def get_download(self):
        if self.download is not None:
            return self.download.path
        else:
            return Download.objects. \
                order_by('?'). \
                first().path
