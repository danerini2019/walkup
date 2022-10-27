from multiprocessing.sharedctypes import SynchronizedString
import requests
from bs4 import BeautifulSoup
import pandas as pd

def main():

    # pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    
    team_lst = ["Angels", "Astros", "Athletics", "BlueJays", "Braves", 
    "Cardinals", "Cubs", "Dbacks", "Dodgers", "Giants", "Guardians",
    "Mariners", "Mets", "Nationals", "Orioles", "Padres",
    "Phillies", "Rangers", "Rays", "Reds", "Rockies",
    "Tigers", "Twins", "Yankees"]

    # team_lst = ['rays']

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

    player_lst = []
    song_lst = []
    for team_name in team_lst: 
        team_name = team_name.lower()
        print(team_name)
        page = requests.get(f'https://www.mlb.com/{team_name}/ballpark/music')
        soup = BeautifulSoup(page.content, 'html.parser')
        stuff = list(soup.children)[1]
        stuff = list(stuff.children)[1]
        player_names = stuff.find_all(class_='u-text-h4 u-text-flow')
        player_songs = stuff.find_all(class_='p-wysiwyg styles-sc-1ewxgrh-0 styles-sc-9861x0-0 bjPBFY gLBcvo')
        songs_p_1 = player_songs[0].find_all('p')
        try:
            if 'by' not in player_songs[0].find('p').get_text():
                player_songs = player_songs[1:]
        except:
            pass

        for i in range(len(player_songs)):
            songs_u_app = player_songs[i].find_all('span', {'class':'u-app-show'})
            songs_p_1 = player_songs[i].find_all('p')
            if stuff.find_all(class_='u-app-show'):
                songs = songs_u_app
                for j in range(len(songs)):
                    try:
                        player_lst.append(player_names[i].get_text().strip())
                        song_lst.append(songs[j].get_text().strip())
                    except:
                        print('index out of range')
                        pass
            elif songs_p_1:
                songs = songs_p_1
                for j in range(len(songs)):
                    try:
                        player_lst.append(player_names[i].get_text().strip())
                        song_lst.append(songs[j].get_text().strip())
                    except:
                        print('non-song entry catured')
                        pass
            # else:
            #     print('else called')
            #     player_lst.append(player_names[i].get_text().strip())
            #     song_lst.append(player_songs[i].get_text().strip())

        # lists of songs and players
        # player_lst.append([player_names[i].get_text() for i in range(len(player_names))])
        # song_lst.append([player_songs[i].get_text() for i in range(len(player_songs))])
        # # print([player_songs[i].get_text() for i in range(len(player_songs))])

    # Bringing values into dataframe and adding rows for players with multiple songs
    # print(player_lst)
    # print(song_lst)
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
        # print(song_lst_clean)
        # print(song_lst[i][j].strip())

    dict = {'players': player_lst_clean,'songs': song_lst_clean}
    # print(len(dict['players']))
    # print(len(dict['songs']))
    # print(dict)

    df = pd.DataFrame(columns = ['players', 'songs'])

    for i in range(len(dict['songs'])):
        # print(f'i={i}')
        if '\n' in dict['songs'][i]:
            plr_song_lst = dict['songs'][i].split('\n\n')
            # print(plr_song_lst)

            for j in range(len(plr_song_lst)):
                # print(f'j={j}')
                append_row_dict = {'players': [dict['players'][i]], 'songs': [plr_song_lst[j]]}
                append_row = pd.DataFrame(append_row_dict)
                # print(append_row)
                df.loc[len(df.index)] = append_row.loc[0]
            
        else:
            # print(f'else i={i}')
            append_row_dict = {'players': [dict['players'][i]], 'songs': [dict['songs'][i]]}
            # print(append_row_dict)
            append_row = pd.DataFrame(append_row_dict)
            # print(append_row)
            df.loc[len(df.index)] = append_row.loc[0]
            
    # print(df.players)
    # print(df.songs)
    print(df)

if __name__ == "__main__":
    main()
