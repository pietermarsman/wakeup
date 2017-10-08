from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from clock.forms import AlarmForm
from clock.models import Alarm


class AlarmList(ListView):
    model = Alarm


class AlarmDetails(DetailView):
    model = Alarm


class AlarmCreate(CreateView):
    model = Alarm
    form_class = AlarmForm
    success_url = '/alarms'
    template_name = 'clock/alarm_form.html'


class AlarmUpdate(UpdateView):
    model = Alarm
    form_class = AlarmForm
    success_url = '/alarms'


class AlarmDelete(DeleteView):
    model = Alarm
    success_url = reverse_lazy('alarm-list')
