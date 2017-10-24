import logging
from flask import Flask
from logger import create_app_log_handler

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('HOCKEYSTATS_CONFIG', silent=True)

app.logger.addHandler(create_app_log_handler(app.config['HOCKEY_STATS_LOG_FILE']))
app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
