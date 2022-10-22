import requests
from bs4 import BeautifulSoup
import pandas as pd

def main():

    pd.set_option('display.max_colwidth', None)
    
    # team_lst = ["Angels", "Astros", "Athletics", "BlueJays", "Braves", 
    # "Cardinals", "Cubs", "Dbacks", "Dodgers", "Giants", "Guardians",
    # "Mariners", "Mets", "Nationals", "Orioles", "Padres",
    # "Phillies", "Rangers", "Rays", "Reds", "Rockies",
    # "Tigers", "Twins", "Yankees"]

    team_lst = ['yankees']

    # team_lst_no_data = ['pirates', 'redsox', 'brewers', 
    #                     'marlins', 'whitesox', 'royals']

    player_lst = []
    song_lst = []
    for team_name in team_lst: 
        team_name = team_name.lower()
        print(team_name)
        page = requests.get(f'https://www.mlb.com/{team_name}/ballpark/music')
        soup = BeautifulSoup(page.content, 'html.parser')

        stuff = list(soup.children)[1]
        # lst = [type(item) for item in list(soup.children)]
        stuff = list(stuff.children)[1]
        player_names = stuff.find_all(class_='u-text-h4 u-text-flow')
        # player_songs = stuff.find_all(class_='u-app-show')
        player_songs_class = stuff.find_all(class_='p-wysiwyg styles-sc-1ewxgrh-0 styles-sc-9861x0-0 bjPBFY gLBcvo')
        player_songs = player_songs_class.find_all(class_='u-app-show')
        print(player_songs)
        if player_songs_class.find_all(class_='u-app-show') == []:
            player_songs = stuff.find_all(class_='p-wysiwyg styles-sc-1ewxgrh-0 styles-sc-9861x0-0 bjPBFY gLBcvo')
            print(player_songs)
        # Different methods of storing song data for each team.
        # Need to find a way to parse out all edge cases for each nested class
        

        # lists of songs and players
        player_lst.append([player_names[i].get_text() for i in range(len(player_names))])
        song_lst.append([player_songs[i].get_text() for i in range(len(player_songs))])
        print([player_songs[i].get_text() for i in range(len(player_songs))])

    # Bringing values into dataframe and adding rows for players with multiple songs
    player_lst_clean = []
    for i in range(len(player_lst)):
        for j in range(len(player_lst[i])):
            player_lst_clean.append(player_lst[i][j].strip())
            # strip isn't necessary at this point but we do need to remove the
            # numbers in front of the names of players on some teams.
            # That logic will appear hear. Looping to accumulate all names in 
            # one list.

    song_lst_clean = []
    for i in range(len(song_lst)):
        for j in range(len(song_lst[i])):
            song_lst_clean.append(song_lst[i][j].strip())
            # print(song_lst[i][j].strip())

    dict = {'players': player_lst_clean,'songs': song_lst_clean}
    # print(len(dict['players']))
    # print(len(dict['songs']))

    df = pd.DataFrame(columns = ['players', 'songs'])

    for i in range(len(dict['songs'])):
        # print(f'i={i}')
        if '\n\n' in dict['songs'][i]:
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
            append_row = pd.DataFrame(append_row_dict)
            # print(append_row)
            df.loc[len(df.index)] = append_row.loc[0]
            
    # print(df.players)
    # print(df.songs)
    # print(df)

if __name__ == "__main__":
    main()
