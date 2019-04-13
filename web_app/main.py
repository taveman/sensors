import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, render_template

app = Flask(__name__)

formatter = logging.Formatter('%(levelname)s [%(funcName)s]: %(asctime)s: %(name)s: %(message)s')
file_info = TimedRotatingFileHandler('/var/log/web/web.log', when='D', interval=1, backupCount=50)
file_info.setLevel(logging.INFO)
app.logger.addHandler(file_info)
app.logger.setLevel(logging.INFO)

app.logger.info('Starting up web application')


@app.route('/')
def controller_app():
    return render_template('controller.html')
