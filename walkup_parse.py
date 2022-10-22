import requests
from bs4 import BeautifulSoup
import pandas as pd

pd.set_option('display.max_colwidth', None)

page = requests.get('https://www.mlb.com/phillies/ballpark/music')
soup = BeautifulSoup(page.content, 'html.parser')

stuff = list(soup.children)[1]
lst = [type(item) for item in list(soup.children)]
stuff = list(stuff.children)[1]
player_names = stuff.find_all(class_='u-text-h4 u-text-flow')
player_songs = stuff.find_all(class_='u-app-show')

# lists of songs and players
player_lst = [player_names[i].get_text() for i in range(len(player_names))]
song_lst = [player_songs[i].get_text() for i in range(len(player_songs))]

# Bringing values into dataframe and adding rows for players with multiple songs
for i in range(len(song_lst)):
    song_lst[i] = song_lst[i].strip()

dict = {'players': player_lst,'songs': song_lst}

df = pd.DataFrame(columns = ['players', 'songs'])

for i in range(len(dict['songs'])):

    if '\n\n' in dict['songs'][i]:
        plr_song_lst = dict['songs'][i].split('\n\n')

        for j in range(len(plr_song_lst)):
            append_row_dict = {'players': [dict['players'][i]], 'songs': [plr_song_lst[j]]}
            append_row = pd.DataFrame(append_row_dict)
            df.loc[len(df.index)] = append_row.loc[0]
        
    else:
        append_row_dict = {'players': [dict['players'][i]], 'songs': [dict['songs'][i]]}
        append_row = pd.DataFrame(append_row_dict)
        df.loc[len(df.index)] = append_row.loc[0]
        
print(df)