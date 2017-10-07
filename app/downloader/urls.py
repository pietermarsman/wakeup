from django.conf.urls import url

from downloader.views import Top40List

urlpatterns = [
    url(r'^$', Top40List.as_view(), name='downloader-list'),
]
