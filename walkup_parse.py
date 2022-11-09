from multiprocessing.sharedctypes import SynchronizedString
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from pprint import pprint

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
    # 1. Angels - default? Accessed by longer class name along
    # 2. As - longer class followed by u-app-show/hide
    #   players with multiple songs - songs in sibling u-app classes
    # 3. Phillies - longer class parent of u-app
    #   multiple songs separated by returns
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
        team_name = team_name.lower()
        print(team_name)
        page = requests.get(f'https://www.mlb.com/{team_name}/ballpark/music')
        soup = BeautifulSoup(page.content, 'html.parser')
        stuff = list(soup.children)[1]
        stuff = list(stuff.children)[1]
        player_names = stuff.find_all(class_='u-text-h4 u-text-flow')
        player_songs = stuff.find_all(class_='p-wysiwyg styles-sc-1ewxgrh-0 styles-sc-9861x0-0 bjPBFY gLBcvo')
        hrefs = list(player_songs)
        try:
            if 'by' not in player_songs[0].find('p').get_text():
                player_songs = player_songs[1:]
        except:
            pass

        for i in range(len(player_songs)):
            # print(f'\n i={i}')
            songs_u_app = player_songs[i].find_all('span', {'class':'u-app-show'})
            # print(songs_u_app)
            songs_p_1 = player_songs[i].find_all('p')
            # print(songs_p_1)
            spotify_url = hrefs[i].find('a')
            if spotify_url == None:
                spotify_url_href = ''
            else:
                spotify_url_href = hrefs[i].find_all('a', href=True)
            print('1')
            print(spotify_url_href)
            print('2')
            
            if songs_u_app:
                songs = songs_u_app
                for j in range(len(songs)):
                    try:
                        print(songs[j].get_text().strip())
                        print(spotify_url_href[j].get('href'))
                        player_lst.append(player_names[i].get_text().strip())
                        song_lst.append(songs[j].get_text().strip())
                        team_name_lst.append(team_name)
                        spotify_link_list.append(spotify_url_href[j].get('href'))
                        
                    except:
                        spotify_link_list.append('')
                        pass
                    
            elif songs_p_1:
                songs = songs_p_1
                for j in range(len(songs)):
                    try:
                        print(songs[j].get_text().strip())
                        print(spotify_url_href[j].get('href'))
                        player_lst.append(player_names[i].get_text().strip())
                        song_lst.append(songs[j].get_text().strip())
                        team_name_lst.append(team_name)
                        spotify_link_list.append(spotify_url_href[j].get('href'))
                    except:
                        spotify_link_list.append('')
                        pass

    # print(spotify_link_list)
    player_lst_clean = []
    for i in range(len(player_lst)):
        player_lst_clean.append(player_lst[i].strip())
            # strip isn't necessary at this point but we do need to remove the
            # numbers in front of the names of players on some teams.
            # That logic will appear hear. Looping to accumulate all names in 
            # one list.

    song_lst_clean = []
    for i in range(len(song_lst)):
        song_lst_clean.append(song_lst[i].strip())

    dict = {'players': player_lst_clean,'songs': song_lst_clean}

    df = pd.DataFrame(columns = ['year', 'team', 'players', 'songs', 'spotify_url'])

    for i in range(len(dict['songs'])):
        # print(f'i={i}')
        if '\n' in dict['songs'][i] and dict['songs'][i].count('by') > 1:
            # print(dict['songs'][i])
            plr_song_lst = dict['songs'][i].split('\n')
            # print(plr_song_lst)

            for j in range(len(plr_song_lst)):
                append_row_dict = {'year': 2022, 'team': team_name_lst[i], 'players': [dict['players'][i]], 'songs': [plr_song_lst[j]], 'spotify_url': [spotify_link_list[i]]}
                append_row = pd.DataFrame(append_row_dict)
                df.loc[len(df.index)] = append_row.loc[0]
            
        else:
            append_row_dict = {'year': 2022, 'team': team_name_lst[i], 'players': [dict['players'][i]], 'songs': [dict['songs'][i]], 'spotify_url': [spotify_link_list[i]]}
            append_row = pd.DataFrame(append_row_dict)
            df.loc[len(df.index)] = append_row.loc[0]
    
    # dropping empty song rows that occurred as a result of splitting above
    df['songs'].replace('', np.nan, inplace=True)
    df.dropna(subset=['songs'], inplace=True)

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
