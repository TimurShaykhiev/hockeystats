import logging
from flask import Flask, current_app, request

from logger import create_rotating_file_handler, create_smtp_handler
from .database import configure_db

HOCKEY_STATS_LOG_FILE = 'webapp.log'


def create_app():
    """Create Flask application."""
    app = Flask('app')
    _configure_app(app)
    _configure_logging(app)
    _configure_blueprints(app)
    _configure_error_handlers(app)
    configure_db(app)
    return app


def _configure_app(app):
    app.config.from_object('config')
    app.config.from_envvar('HOCKEYSTATS_APP_CONFIG', silent=True)


def _configure_logging(app):
    log_level = getattr(logging, app.config['HOCKEY_STATS_LOG_LEVEL'])
    log_file_path = app.config['LOG_DIR'] + HOCKEY_STATS_LOG_FILE

    app.logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s [%(module)s:%(lineno)d]')

    rfh = create_rotating_file_handler(log_file_path)
    rfh.setLevel(log_level)
    rfh.setFormatter(formatter)
    app.logger.addHandler(rfh)

    email_handler = create_smtp_handler(app.config, 'WebApp:Error')
    email_handler.setLevel(logging.ERROR)
    app.logger.addHandler(email_handler)

    @app.before_request
    def log_request():
        current_app.logger.debug(request.url)


def _configure_blueprints(flask_app):
    import app.api as api
    flask_app.register_blueprint(api.season_stats_api)
    flask_app.register_blueprint(api.season_api)
    flask_app.register_blueprint(api.team_api)
    flask_app.register_blueprint(api.skater_api)
    flask_app.register_blueprint(api.goalie_api)
    flask_app.register_blueprint(api.teams_api)
    flask_app.register_blueprint(api.skaters_api)
    flask_app.register_blueprint(api.goalies_api)


def _configure_error_handlers(flask_app):
    from app.api.response_utils import ApiError

    @flask_app.errorhandler(ApiError)
    def handle_invalid_usage(error):
        current_app.logger.error('Request failed %s, %s', error.status_code, error.api_err_code)
        return error.get_response()
