import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, current_app, request

from .database import configure_db


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
    app.config.from_envvar('HOCKEYSTATS_CONFIG', silent=True)


def _configure_logging(app):
    log_size_limit = 50 * 1024 * 1024
    backup_count = 5
    log_level = getattr(logging, app.config['HOCKEY_STATS_LOG_LEVEL'])

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s [%(module)s:%(lineno)d]')
    rfh = RotatingFileHandler(app.config['HOCKEY_STATS_LOG_FILE'], maxBytes=log_size_limit, backupCount=backup_count)
    rfh.setLevel(log_level)
    rfh.setFormatter(formatter)

    app.logger.addHandler(rfh)
    app.logger.setLevel(log_level)

    @app.before_request
    def log_request():
        current_app.logger.debug(request.url)


def _configure_blueprints(app):
    import api
    app.register_blueprint(api.season_stats_api)
    app.register_blueprint(api.season_api)


def _configure_error_handlers(app):
    from api.response_utils import ApiError

    @app.errorhandler(ApiError)
    def handle_invalid_usage(error):
        current_app.logger.error('Request failed %s, %s', error.status_code, error.api_err_code)
        return error.get_response()
