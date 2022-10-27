import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config
import sys
from pprint import pprint

#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=config.cid, client_secret=config.cid_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
print(sys.argv)
if len(sys.argv) > 1:
    artist = sys.argv[2]
    song = sys.argv[1]
    q = "remaster%20track:Doxy%20artist:Miles%20Davis"
    results = sp.search(q, limit=20)
    print(results)
    for i, t in enumerate(results['tracks']['items']):
        print(' ', i, t['name'])

