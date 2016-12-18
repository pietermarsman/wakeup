import datetime

from flask import Flask, jsonify
from flask import make_response
from flask import redirect
from flask_httpauth import HTTPBasicAuth

from alarmclock import AlarmClock

context = ('/home/pieter/other/certificates/server.crt',
           '/home/pieter/other/certificates/server.key')

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
