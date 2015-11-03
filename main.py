from datetime import datetime
from time import strftime
from time import localtime
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import SelectField, SubmitField
from wtforms.validators import Required

from utils import get_weather_json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class CityForm(Form):
    city = SelectField("City", choices=[(None, ""), ("newyork,us", "New York"),("naugatuck,us", "Naugatuck"),("sanfrancisco,us", "San Francisco")])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    if app.test_request_context(method='POST'):
        form = CityForm(default=session.get('city'))
    else:
        form = CityForm()
        
    if form.validate_on_submit():
        old_city = session.get('city')
        session['city'] = form.city.data
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           weather_json=get_weather_json(session.get('city')),
                           strftime=strftime,
                           localtime=localtime,
                           form=form)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    manager.run()
