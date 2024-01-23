import config
from flask import Flask, redirect, url_for
from flask_session import Session

from . import chatgpt_api
from . import spotify_api

def create_app():
    app = Flask(__name__)

    # Set API keys
    api_keys_path = './spotify_playlist_recommender/api_keys.cfg'
    api_keys = config.Config(api_keys_path)
    spotify_api.authenticate_spotify(api_keys['SPOTIFY_CLIENT_ID'], api_keys['SPOTIFY_CLIENT_SECRET'])
    chatgpt_api.authenticate_openai(api_keys['OPENAI_API_KEY'])

    # Configure server-side session
    app.secret_key = 'super secret key' # TODO: use an actual secret key
    app.config['SESSION_TYPE'] = 'filesystem' # TODO: manage app config in a separate file https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-files
    sess = Session()
    sess.init_app(app)

    with app.app_context():
        from . import routes

        app.register_blueprint(routes.main_blueprint)

        return app
