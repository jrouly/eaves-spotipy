from flask import Flask, jsonify, request, render_template
import spotipy
import spotipy.util as util
import os

app = Flask(__name__)

app.config['APPLICATION_ROOT'] = '/spotify'

@app.route('/')
def home():
    return 'hello world'

@app.route('/search', methods = ['GET', 'POST'])
def search():

    if request.method == 'GET':
        return render_template('search.html')

    query = request.form['query']
    sp = spotipy.Spotify()
    result = sp.search(query)
    tracks = result.get('tracks')
    if tracks is None:
        return render_template('search.html', results = [])

    items = map(lambda item: {
        'name': item.get('name'),
        'id': item.get('id')
    }, tracks.get('items'))
    return render_template('search.html', query = query, results = items)

@app.route('/play', methods = ['GET'])
def play(song_id):

    username = os.getenv('EAVES_USERNAME')
    playlist_id = os.getenv('EAVES_PLAYLIST_ID')
    
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope)
    
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, playlist_id, song_id)
        print results
    else:
        print 'Can't get token for', username


if __name__ == '__main__':
    app.run(port = 8000, debug = True)
