from django.conf.urls import url

from top40.views import Top40List

urlpatterns = [
    url(r'^$', Top40List.as_view(), name='top40-list'),
]
