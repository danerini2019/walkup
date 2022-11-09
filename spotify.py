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
print('df')
print(df.shape[0])

# print(df[['team', 'players', 'artist','songs']].iloc[310:320])

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
api_song_name = []
api_artist_name = []
results = {}

df_snippet = df.iloc[:20]
for index, row in df_snippet.iterrows():
    artist = row['artist']
    print(artist)
    song = row['songs']
    print(song)
    results = sp.search(q="artist:" + artist + " track:" + song, type="track")
    # print(results)
    # print(song)
    # print(f'track_id: {len(track_id)}')
    # print(f'popularity: {len(popularity)}')
    # print(f'artist_genres: {len(artist_genres)}')
    # pprint(f'song_name: {api_song_name}\n')
    # pprint(f'artist: {api_artist_name}\n')
    # print(f'popularity: {popularity}\n')
    # print(f'artist_genres: {artist_genres}\n')
    # print(f'album_release_date: {album_release_date}\n')
    pprint(results['tracks']['items'])
   
    if results['tracks']['items'] != []:
        print('song matches \n')
        track_id.append(results['tracks']['items'][0]['id'])
        api_song_name.append(results['tracks']['items'][0]['name'])
        api_artist_name.append(results['tracks']['items'][0]['artists'][0]['name'])
        popularity.append(results['tracks']['items'][0]['popularity'])
        uri.append(results['tracks']['items'][0]['uri'])
        explicit.append(results['tracks']['items'][0]['explicit'])
        duration_ms.append(results['tracks']['items'][0]['duration_ms'])
        spotify_url.append(results['tracks']['items'][0]['external_urls']['spotify'])
        album_release_date.append(results['tracks']['items'][0]['album']['release_date'])
    else:
        print('song does not match\n')
        no_results_list.append([artist, song])
        track_id.append('')
        popularity.append('')
        uri.append('')
        explicit.append('')
        duration_ms.append('')
        spotify_url.append('')
        album_release_date.append('')
    

print('api adds')
pprint(no_results_list)
pprint(track_id)
pprint(api_song_name)
pprint(api_artist_name)
pprint(popularity)
pprint(uri)
pprint(explicit)
pprint(duration_ms)
pprint(duration_ms)
pprint(spotify_url)
pprint(album_release_date)


# print(track_id[:5])
# print(artist_genres[:5])

# df.insert(loc=len(df.columns), column='track_id', value=track_id)
# print(df.head())
# artist = 'Ruben Blades'
# song = 'Patira'
# results = sp.search(q="artist:" + artist + " track:" + song, type="track")
# print(results['tracks']['items'])
# # print(type(results))
# df['track_id'] = results['tracks']['items'][0]['id']


# ['name', 'popularity', 'uri', 'explicit', 'duration_ms']
# print(df['songs'][df.songs == 'Dior'])
