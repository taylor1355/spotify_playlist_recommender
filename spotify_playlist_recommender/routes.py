from flask import Blueprint, render_template, request, session, flash, redirect, url_for

from . import spotify_api

main_blueprint = Blueprint(
    'main_blueprint', __name__,
    template_folder='templates'
)

@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    # redirect to search page
    return redirect(url_for('main_blueprint.search_playlists'))
    # return render_template('index.html')

# TODO: change function names to lookup_playlist and add_playlist
@main_blueprint.route('/search-playlists', methods=['GET', 'POST'])
def search_playlists():
    display_info = None
    if request.method == 'POST':
        playlist_id = request.form['playlistId']
        playlist_info = spotify_api.get_playlist_details(playlist_id)
        session['playlist_info'] = playlist_info
        display_info = {
            'name': playlist_info['name'],
            'owner': playlist_info['owner']['display_name'],
            'description': playlist_info['description'],
            'num_tracks': playlist_info['tracks']['total'],
        }
    return render_template('add_playlist.html', playlist_info=display_info)

@main_blueprint.route('/add-playlist', methods=['POST'])
def add_playlist():
    playlist_id = session['playlist_info']['id']
    if playlist_id:
        if 'playlists' not in session:
            session['playlists'] = {}
        session['playlists'][playlist_id] = session['playlist_info']
        new_playlist_name = session['playlist_info']['name']
        flash(f'Playlist "{new_playlist_name}" added successfully!', 'success')
    return render_template('add_playlist.html')