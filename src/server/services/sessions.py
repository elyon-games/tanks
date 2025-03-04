from flask_session import Session as FlaskSession
import common.path as path
from common.config import getConfig

def initSessions(app):
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = path.get_path('server_sessions')
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_SECRET_KEY'] = getConfig("server")['secret']
    FlaskSession(app)