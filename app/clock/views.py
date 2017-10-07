from django.shortcuts import render

# Create your views here.


class AlarmClock(Thread, Scheduler):
    def __init__(self, song_type='top40', **kwargs):
        super(AlarmClock, self).__init__()
        Scheduler.__init__(self)
        self.alarm_type = song_type
        self.audio_mixer = AudioMixerFactory.get_mixer()
        self.kwargs = kwargs

    def run(self):
        while True:
            self.run_pending()
            time.sleep(1)

    def run_alarm_now(self):
        AlarmClock.run_thread(True)(self.song_type_func())

    def set_single_alarm(self, t, day=None):
        if day is None:
            self.every().day.at(t).do(AlarmClock.run_thread(True),
                                      self.song_type_func())
        else:
            job = self.every()
            job.unit = 'weeks'
            job.start_day = day
            job.at(t).do(AlarmClock.run_thread(True), self.song_type_func())

    def remove_single_alarm(self, i):
        if i < len(self.jobs):
            self.cancel_job(self.jobs[i])

    def snooze(self, duration):
        self.stop()
        self.every(duration).minutes.do(AlarmClock.run_thread(True),
                                        self.song_type_func())

    def stop(self):
        self.audio_mixer.fadeout_music()

    def song_type_func(self):
        if self.alarm_type is 'top40':
            return Top40YoutubeAlarm(self.audio_mixer, **self.kwargs)
        else:
            return YoutubeAlarm(self.alarm_type, self.audio_mixer,
                                **self.kwargs)

    def jsonify(self):
        return {'alarms': str(self.jobs), 'alarm_type': self.alarm_type}

    @staticmethod
    def run_thread(once):
        def func(thread_obj):
            thread_obj.start()
            if once:
                return CancelJob

        return func

import datetime

from flask import Flask, jsonify
from flask import make_response
from flask import redirect
from flask_httpauth import HTTPBasicAuth

from alarmclock import AlarmClock

from args import context

alarm = AlarmClock('top40')

app = Flask(__name__)
app.secret_key = 'pietersecretkey'
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'pieter':
        return 'wakemeup'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


def get_state():
    json_state = {'instructions': {
        'set alarm': ['/alarm/<int:hour>/<int:minute>',
                      '/alarm/<string:day>/<int:hour>/<int:minute>'],
        'snooze alarm': ['/snooze', '/snooze/<int:duration>'],
        'stop alarm': ['/stop'],
        'change alarm type': ['/alarm_type/<str:alarm_type>'],
        'remove alarm': ['/remove/<int:i>']}, 'state': alarm.jsonify(),
        'time': datetime.datetime.now()}
    return jsonify(json_state)


@app.route('/')
@auth.login_required
def index():
    return get_state()


@app.route('/alarm/<string:day>/<int:hour>/<int:minute>')
@app.route("/alarm/<int:hour>/<int:minute>")
@app.route('/alarm/now')
@auth.login_required
def set_alarm(hour=None, minute=None, day=None):
    if hour is None and minute is None and day is None:
        alarm.run_alarm_now()
    else:
        alarm.set_single_alarm('%.2d:%.2d' % (hour, minute), day)
    return redirect("/", code=302)


@app.route('/remove/<int:i>')
@auth.login_required
def remove_alarm(i):
    alarm.remove_single_alarm(i)
    return redirect("/", code=302)


@app.route("/snooze")
@app.route("/snooze/<int:duration>")
@auth.login_required
def snooze(duration=5):
    alarm.snooze(duration)
    return redirect("/", code=302)


@app.route("/stop")
@auth.login_required
def stop_alarm():
    alarm.stop()
    return redirect("/", code=302)


@app.route('/alarm_type/<string:alarm_type>')
@auth.login_required
def change_alarm_type(alarm_type):
    alarm.alarm_type = alarm_type
    return redirect("/", code=302)


if __name__ == "__main__":
    alarm.start()
    app.run(host='0.0.0.0', debug=True, ssl_context=context, threaded=True)
