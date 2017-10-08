from django.conf.urls import url

from clock.views import AlarmList, AlarmDetails, AlarmCreate, AlarmUpdate, AlarmDelete

urlpatterns = [
    url(r'^$', AlarmList.as_view(), name='alarm-list'),
    url(r'^(?P<pk>[0-9]+)/$', AlarmDetails.as_view(), name='alarm-detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', AlarmUpdate.as_view(), name='alarm-form-edit'),
    url(r'^(?P<pk>[0-9]+)/delete/$', AlarmDelete.as_view(), name='alarm-form-delete'),
    url(r'^new/$', AlarmCreate.as_view(), name='alarm-form'),
]
