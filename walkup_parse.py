from multiprocessing.sharedctypes import SynchronizedString
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from pprint import pprint
import sys

def main():

    # pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    
    # team_lst = ["Angels", "Astros", "Athletics", "BlueJays", "Braves", 
    # "Cardinals", "Cubs", "Dbacks", "Dodgers", "Giants", "Guardians",
    # "Mariners", "Mets", "Nationals", "Orioles", "Padres",
    # "Phillies", "Rangers", "Rays", "Reds", "Rockies",
    # "Tigers", "Twins", "Yankees"]

    team_lst = ['yankees']

    # teams_need_work = ['mets',']

    # team_lst_no_data = ['pirates', 'redsox', 'brewers', 
    #                     'marlins', 'whitesox', 'royals']

    # song name get output types
    # 1. Angels - default? Accessed by longer class name alone
    # 2. As - longer class followed by u-app-show/hide
    #   players with multiple songs - songs in sibling u-app classes
    # 3. Phillies - longer class parent of u-app
    #   multiple songs separated by returns
    #   no spotify links
    # 4. Yankees - song not available - example in yanks, accessed by long 
    # in this case but could also appear in other forms
    # 5. Braves - longer class followed by u-app-show/hide
    #   players with multiple songs - songs in same u-app class
    # 6. Bluejays - some second songs are stored in a u-app-hide class
        # can't pull from all u-app-hide and show classes? ignore for now

    player_lst = []
    song_lst = []
    team_name_lst = []
    spotify_link_list = []
    for team_name in team_lst: 
        print(team_name)
        with open(f'site_output/{team_name}.html', 'r') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            
        stuff = list(soup.children)[1]
        stuff = list(stuff.children)[1]
        player_names = stuff.find_all(class_='u-text-h4 u-text-flow')
        player_songs = stuff.find_all(class_='p-wysiwyg styles-sc-1ewxgrh-0 styles-sc-9861x0-0 bjPBFY gLBcvo')
        hrefs = list(player_songs)
        print(player_songs)
        try:
            if 'by' not in player_songs[0].find('p').get_text():
                player_songs = player_songs[1:]
        except:
            pass

    for i in range(len(player_songs)):
        print(f'\n i={i}')
        print(f'player name:{player_names[i].get_text().strip()}')
        songs_u_app = player_songs[i].find_all('span', {'class':'u-app-hide'})
        # songs_u_app = str(songs_u_app).split('<br/><br/>', 1)

        print(f'songs:{songs_u_app}')
        print('\n')
        print(type(songs_u_app))
        print(f'num of songs: {len(songs_u_app)}')
        songs_p_1 = player_songs[i].find_all('p')
        spotify_url = hrefs[i].find('a')
        if spotify_url == None:
            print('heallo')
            spotify_url_href = ''
        else:
            spotify_url_href = hrefs[i].find_all('a', href=True)
        print(f'spotify href:{spotify_url_href}')
        print(f'num spotify links: {len(spotify_url_href)}')
        if songs_u_app:
            songs = list(songs_u_app)
            for j in range(len(songs)):
                if len(spotify_url_href) > 0:
                    print(songs[j].get_text().strip())
                    print(spotify_url_href[j])
                    try:
                        song_name_append = songs[j].get_text().strip()
                        spotify_url_append = spotify_url_href[j]
                    except:
                        print('more songs than links')
                        spotify_url_append = ''

                else:
                    spotify_link_list.append('')
                try:
                    print(song_name_append)
                    print(spotify_url_append)
                    player_lst.append(player_names[i].get_text().strip())
                    song_lst.append(song_name_append)
                    team_name_lst.append(team_name)
                    spotify_link_list.append(spotify_url_append)
                except:
                    print('something didn''t pass')
                    pass
                
        elif songs_p_1:
            songs = list(songs_p_1)
            for j in range(len(songs)):
                if len(spotify_url_href) > 0:
                    print(spotify_url_href[j])
                    spotify_link_list.append(spotify_url_href[j])
                else:
                    spotify_link_list.append('')
                try:
                    # print(songs[j].get_text().strip())
                    player_lst.append(player_names[i].get_text().strip())
                    song_lst.append(songs[j].get_text().strip())
                    team_name_lst.append(team_name)
                except:
                    print('something didn''t pass')
                    pass

    player_lst_clean = []
    for i in range(len(player_lst)):
        player_lst_clean.append(player_lst[i].strip())

    song_lst_clean = []
    for i in range(len(song_lst)): 
        song_lst_clean.append(song_lst[i].strip())

    dict = {'players': player_lst_clean,'songs': song_lst_clean}

    df = pd.DataFrame(columns = ['year', 'team', 'players', 'songs', 'spotify_url'])

    for i in range(len(dict['songs'])):
        print(f'i={i}')
        print(player_names[i].get_text().strip())
        print(spotify_link_list[i])
        if spotify_link_list[i] != '':
            print(spotify_link_list[i].get('href'))
            print(spotify_link_list[i].find('em').contents)
        if '\n' in dict['songs'][i] and dict['songs'][i].count('by') > 1:
            # print(dict['songs'][i])
            plr_song_lst = dict['songs'][i].split('\n')
            # print(plr_song_lst)

            for j in range(len(plr_song_lst)):
                print(spotify_link_list[i][j])
                # how to tell which spotify link goes to which song if there are less links than songs
                if spotify_link_list[i][j] != '':
                    spotify_url_entry = spotify_link_list[i][j].get('href')
                else:
                    spotify_url_entry = spotify_link_list[i][j]
                append_row_dict = {'year': 2022, 'team': team_name_lst[i], 'players': [dict['players'][i]], 'songs': [plr_song_lst[j]], 'spotify_url': [spotify_url_entry]}
                append_row = pd.DataFrame(append_row_dict)
                df.loc[len(df.index)] = append_row.loc[0]
            
        else:
            # print(spotify_link_list[i])
            if spotify_link_list[i] != '':
                    spotify_url_entry = spotify_link_list[i].get('href')
            else:
                spotify_url_entry = spotify_link_list[i]
            append_row_dict = {'year': 2022, 'team': team_name_lst[i], 'players': [dict['players'][i]], 'songs': [dict['songs'][i]], 'spotify_url': [spotify_url_entry]}
            append_row = pd.DataFrame(append_row_dict)
            df.loc[len(df.index)] = append_row.loc[0]
    
    # dropping empty song rows that occurred as a result of splitting above
    # df['songs'].replace('', np.nan, inplace=True)
    # df['songs'].replace('Song Not Available', np.nan, inplace=True)
    # df.dropna(subset=['songs'], inplace=True)

    # getting rid of number in front of nationals players names
    nats_players_clean = []
    for player in df['players'][df.team == 'nationals']:
        name_start_index = player.find(next(filter(str.isalpha, player)))
        nats_players_clean.append(player[name_start_index:])
    
    df['players'][df.team == 'nationals'] = nats_players_clean

    # Split songs and artists
    df['artist'] = df['songs'].str.split(n=2, pat='by', expand=True)[1].str.strip()
    df['songs'] = df['songs'].str.split(n=2, pat='by', expand=True)[0].str.strip()

    print(df)
    df.to_pickle('walkup_song_df.pkl')
    return df

if __name__ == "__main__":
    main()
