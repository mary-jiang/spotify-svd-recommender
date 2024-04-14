from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_data(search):
    conn = sqlite3.connect('spotify.db')
    cur = conn.cursor()
    cur.execute("SELECT track_name, artist_name FROM tracks WHERE track_name LIKE ? OR artist_name LIKE ? LIMIT 20", ('%' + search + '%', '%' + search + '%'))
    data = cur.fetchall()
    conn.close()
    return [' - '.join(row) for row in data]

def song_exists(song, artist):
    conn = sqlite3.connect('spotify.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tracks WHERE track_name = ? AND artist_name = ?", (song, artist))
    count = cur.fetchone()[0]
    conn.close()
    return count > 0


@app.route('/')
def index():
    return render_template('index.html')

# autocomplete route
@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        results = get_data(query)
    else:
        results = []
    return jsonify(matching_results=results)

# TODO: link with SVD method to return recommendation results
@app.route('/recommend')
def recommend():
    selected_song = request.args.get('selected_song')
    if selected_song:
        track_song, sep, track_artist = selected_song.rpartition(' - ')
        track_song = track_song.strip()
        track_artist = track_artist.strip()
        print('selected song: {} selected artist: {}'.format(track_song, track_artist))
        if sep and song_exists(track_song, track_artist):
            recommendations = [
                {"song_name": "Song One", "score": 88},
                {"song_name": "Song Two", "score": 92},
                {"song_name": "Song Three", "score": 85}
            ]
            return jsonify(recommendations)
        else:
            return jsonify({'error': 'Song or artist not found or invalid format'}), 400
    else:
        return jsonify({'error': 'No song provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
