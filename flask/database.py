import pandas as pd
import sqlite3

# This file is used for creating a database containing the track title and artist. 
# Will be used for autocomplete.
try:
    df = pd.read_csv('spotify-2023.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('spotify-2023.csv', encoding='iso-8859-1')

data_to_store = df[['track_name'] + ['artist(s)_name']]
data_to_store = data_to_store.rename(columns={'artist(s)_name': 'artist_name'})

conn = sqlite3.connect('spotify.db')

data_to_store.to_sql('tracks', conn, if_exists='replace', index=False)

conn.close()
