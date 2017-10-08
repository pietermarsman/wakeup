from datetimewidget.widgets import DateTimeWidget
from django.forms import ModelForm

from clock.models import Alarm


class AlarmForm(ModelForm):
    class Meta:
        model = Alarm
        fields = ['datetime', 'download']
        widgets = {
            'datetime': DateTimeWidget(options={'format': 'yyyy-mm-dd HH:ii'}, bootstrap_version=3)
        }
