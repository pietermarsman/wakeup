import datetime

from flask import Flask, jsonify

from alarmclock import AlarmClock

alarm = AlarmClock('top40')
app = Flask(__name__)


def get_state():
    json_state = {
        'instructions': {'set alarm': ['/alarm/<int:hour>/<int:minute>',
                                       '/alarm/<string:day>/<int:hour>/<int:minute>'],
            'snooze alarm': ['/snooze', '/snooze/<int:duration>'],
            'stop alarm': ['/stop'],
            'change alarm type': ['/alarm_type/<str:alarm_type>'],
                         'remove alarm': ['/remove/<int:i>']},
        'state': alarm.jsonify(), 'time': datetime.datetime.now()}
    return jsonify(json_state)


@app.route('/')
def index():
    return get_state()


@app.route('/alarm/<string:day>/<int:hour>/<int:minute>')
@app.route("/alarm/<int:hour>/<int:minute>")
def set_alarm(hour, minute, day=None):
    alarm.set_single_alarm('%.2d:%.2d' % (hour, minute), day)
    return get_state()


@app.route('/remove/<int:i>')
def remove_alarm(i):
    alarm.remove_single_alarm(i)
    return get_state()


@app.route("/snooze")
@app.route("/snooze/<int:duration>")
def snooze(duration=5):
    alarm.snooze(duration)
    return get_state()


@app.route("/stop")
def stop_alarm():
    alarm.stop()
    return get_state()


@app.route('/alarm_type/<string:alarm_type>')
def change_alarm_type(alarm_type):
    alarm.alarm_type = alarm_type
    return get_state()


if __name__ == "__main__":
    alarm.start()
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0')
