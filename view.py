import datetime

import flask
from flask import Flask, jsonify
from flask import redirect
from flask_login import login_required, LoginManager, login_user, logout_user, \
    current_user

from alarmclock import AlarmClock
from user import User

context = ('/home/pieter/other/certificates/server.crt',
           '/home/pieter/other/certificates/server.key')

login_manager = LoginManager()
alarm = AlarmClock('top40')

app = Flask(__name__)
app.secret_key = 'pietersecretkey'


def get_state():
    json_state = {'instructions': {
        'set alarm': ['/alarm/<int:hour>/<int:minute>',
                      '/alarm/<string:day>/<int:hour>/<int:minute>'],
        'snooze alarm': ['/snooze', '/snooze/<int:duration>'],
        'stop alarm': ['/stop'],
        'change alarm type': ['/alarm_type/<str:alarm_type>'],
        'remove alarm': ['/remove/<int:i>']}, 'state': alarm.jsonify(),
        'user': {'logged_in': current_user.is_authenticated},
        'time': datetime.datetime.now()}
    return jsonify(json_state)


@app.route('/login/<string:password>')
def login(password):
    if password == "wakemeup":
        login_user(load_user("1"))

        next = flask.request.args.get('next')
        return flask.redirect(next or flask.url_for('index'))
    return get_state()


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
@login_required
def index():
    return get_state()


@app.route('/alarm/<string:day>/<int:hour>/<int:minute>')
@app.route("/alarm/<int:hour>/<int:minute>")
@login_required
def set_alarm(hour, minute, day=None):
    alarm.set_single_alarm('%.2d:%.2d' % (hour, minute), day)
    return get_state()


@app.route('/remove/<int:i>')
@login_required
def remove_alarm(i):
    alarm.remove_single_alarm(i)
    return get_state()


@app.route("/snooze")
@app.route("/snooze/<int:duration>")
@login_required
def snooze(duration=5):
    alarm.snooze(duration)
    return get_state()


@app.route("/stop")
@login_required
def stop_alarm():
    alarm.stop()
    return get_state()


@app.route('/alarm_type/<string:alarm_type>')
@login_required
def change_alarm_type(alarm_type):
    alarm.alarm_type = alarm_type
    return get_state()


if __name__ == "__main__":
    alarm.start()
    login_manager.init_app(app)
    app.run(host='0.0.0.0', debug=True, ssl_context=context)
