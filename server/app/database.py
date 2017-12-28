from flask import g, current_app
import MySQLdb as Db


def configure_db(app):
    @app.teardown_appcontext
    def close_db(error):
        """Closes the database at the end of the request."""
        if hasattr(g, 'hock_stats_db'):
            g.hock_stats_db.close()


def connect_db():
    """Connects to the specific database."""
    # todo: Think of using DB connection pool
    db_conn = Db.connect(current_app.config['DB_URL'], current_app.config['DB_USER'],
                         current_app.config['DB_PASSWORD'], current_app.config['DB_NAME'], charset='utf8')
    return db_conn


def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'hock_stats_db'):
        g.hock_stats_db = connect_db()
    return g.hock_stats_db
