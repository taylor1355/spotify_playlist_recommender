import pprint
import config

import spotify_api
import chatgpt_api


def describe_tracks(playlist_ids, max_tracks):
    # the output of get_playlist_tracks is a list of dicts, each with a 'track' key
    tracks = []
    for playlist_id in playlist_ids:
        playlist_tracks = spotify_api.get_playlist_tracks(playlist_id)
        tracks.extend(playlist_tracks)
    tracks = tracks[:max_tracks]
    # TODO: deduplicate tracks
    track_descriptions = {}
    for track in tracks:
        id = track['id']
        name = track['name']
        artist = track['artists'][0]['name']
        track_descriptions[id] = chatgpt_api.get_track_description(f'{name} by {artist}')
    return track_descriptions


def describe_playlists(playlist_ids):
    playlist_descriptions = {}
    for playlist_id in playlist_ids:
        playlist_details = spotify_api.get_playlist_details(playlist_id)
        playlist_name = playlist_details['name']
        tracks = spotify_api.get_playlist_tracks(playlist_id)
        playlist_info = {
            'name': playlist_name,
            'tracks': [{'artist': track['artists'][0]['name'], 'title': track['name']} for track in tracks]
        }
        playlist_str = pprint.pformat(playlist_info)
        playlist_descriptions[playlist_id] = chatgpt_api.get_playlist_description(playlist_str)
    return playlist_descriptions


# TODO: Train a model to predict the score based on the playlist and track descriptions
# TODO: Use score -1 when a track is already in a playlist and avoid passing to the LLM
def score_playlist_fits(track_descriptions, playlist_descriptions):
    scores = {}
    for track_id, track_description in track_descriptions.items():
        scores[track_id] = {
            id: chatgpt_api.evaluate_playlist_fit(playlist_description, track_description)
            for id, playlist_description in playlist_descriptions.items()
        }
    return scores


def main():
    # TODO: do not hardcode absolute path, instead use relative path from project root
    api_keys_path = '/home/taylor/projects/spotify_playlist_recommender/src/api_keys.cfg'
    api_keys = config.Config(api_keys_path)
    spotify_api.authenticate_spotify(api_keys['SPOTIFY_CLIENT_ID'], api_keys['SPOTIFY_CLIENT_SECRET'])
    chatgpt_api.authenticate_openai(api_keys['OPENAI_API_KEY'])

    source_playlist_ids = ['67TebCgdO78QYHobH1oGqf'] #input("Enter the Source Playlist IDs (comma-separated): ").split(',')
    destination_playlist_ids = ['4NLRzU1Cf4CwsQQsJCFcPj'] #input("Enter Destination Playlist IDs (comma-separated): ").split(',')

    user_playlists = spotify_api.get_user_playlists('taylor1355')
    for playlist in user_playlists['items']:
        print(f"Name: {playlist['name']}, Id: {playlist['id']}")

    # TODO: cache track descriptions
    max_tracks = 5
    source_track_descriptions = describe_tracks(source_playlist_ids, max_tracks)
    destination_playlist_descriptions = describe_playlists(destination_playlist_ids)

    # Rate how well each source track fits into each destination playlist
    playlist_fit_scores = score_playlist_fits(
        source_track_descriptions,
        destination_playlist_descriptions
    )

    # Display recommendations
    for track_id, scores in playlist_fit_scores.items():
        print(f'Track {track_id} playlist fit scores:')
        pprint.pprint(scores)
        print()

if __name__ == "__main__":
    main()