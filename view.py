import datetime

from flask import Flask, jsonify

from alarmclock import AlarmClock

alarm = AlarmClock()

app = Flask(__name__)
app.config['DEBUG'] = True


def get_state():
    json_state = {'instructions': {'set alarm': ['/alarm/<string:time>'],
                                   'snooze alarm': ['/snooze',
                                                    '/snooze/<int:duration>'],
                                   'stop alarm': ['/stop']},
                  'alarm': str(alarm.jobs), 'time': datetime.datetime.now()}
    return jsonify(json_state)


@app.route('/')
def index():
    return get_state()


@app.route("/alarm/<string:time>")
def set_alarm(time):
    alarm.set_single_alarm(time)
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


if __name__ == "__main__":
    alarm.start()
    app.run(host='0.0.0.0')
