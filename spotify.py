import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config
import sys
from pprint import pprint
import os
import pandas as pd
from walkup_parse import main

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', None)

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=config.cid, client_secret=config.cid_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# dataframe of walkup songs
df = pd.read_pickle('walkup_song_df.pkl')

print(df[['team', 'players', 'artist','songs']].iloc[310:320])

no_results_list = []
track_id = []
popularity = []
uri =[]
explicit = []
duration_ms = []
spotify_url = []
album_release_date = []
artist_followers = []
artist_genres = []
artist_popularity = []


# df_snippet = df.iloc[:5]
# print(df_snippet)
for index, row in df.iterrows():
    artist = row['artist']
    # print(artist)
    song = row['songs']
    # print(song)
    try:
        results = sp.search(q="artist:" + artist + " track:" + song, type="track")
        track_id.append(results['tracks']['items'][0]['id'])
        popularity.append(results['tracks']['items'][0]['popularity'])
        uri.append(results['tracks']['items'][0]['uri'])
        explicit.append(results['tracks']['items'][0]['explicit'])
        duration_ms.append(results['tracks']['items'][0]['duration_ms'])
        spotify_url.append(results['tracks']['items'][0]['external_urls']['spotify'])
        album_release_date.append(results['tracks']['items'][0]['album']['release_date'])
        artist_followers.append(results['tracks']['items'][0]['artists']['followers']['total'])
        artist_genres.append(results['tracks']['items'][0]['artists']['genres'])
        artist_popularity.append(results['tracks']['items'][0]['artists']['popularity'])
    except:
        no_results_list.append([artist, song])
        track_id.append(None)
        popularity.append(None)
        uri.append(None)
        explicit.append(None)
        duration_ms.append(None)
        spotify_url.append(None)
        album_release_date.append(None)
        artist_followers.append(None)
        artist_genres.append(None)
        artist_popularity.append(None)

print(len(track_id))
print(len(no_results_list))

df.insert(loc=len(df.columns), column='track_id', value=track_id)
print(df.head())
# artist = 'Ruben Blades'
# song = 'Patira'
# results = sp.search(q="artist:" + artist + " track:" + song, type="track")
# print(results['tracks']['items'])
# # print(type(results))
# df['track_id'] = results['tracks']['items'][0]['id']


# ['name', 'popularity', 'uri', 'explicit', 'duration_ms']
# print(df['songs'][df.songs == 'Dior'])
