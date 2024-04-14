import pandas as pd
import sqlite3

# This file is used for creating a database using the csv file.
try:
    df = pd.read_csv('spotify-2023.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('spotify-2023.csv', encoding='iso-8859-1')

# Rename columns that include %
column_renames = {
    'artist(s)_name': 'artist_name',
    'danceability_%': 'danceability',
    'valence_%': 'valence',
    'energy_%': 'energy',
    'acousticness_%': 'acousticness',
    'instrumentalness_%': 'instrumentalness',
    'liveness_%': 'liveness',
    'speechiness_%': 'speechiness'
}
df.rename(columns=column_renames, inplace=True)

conn = sqlite3.connect('spotify.db')
df.to_sql('tracks', conn, if_exists='replace', index=False)
conn.close()
