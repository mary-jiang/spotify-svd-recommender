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
    query = request.args.get('song_name')
    #SVD method goes here
    pass
    # return array of recommendations

if __name__ == '__main__':
    app.run(debug=True)
