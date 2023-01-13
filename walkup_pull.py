from multiprocessing.sharedctypes import SynchronizedString
import requests
from bs4 import BeautifulSoup
from pprint import pprint

def main():

    # team_lst = ["Angels", "Astros", "Athletics", "BlueJays", "Braves", 
    # "Cardinals", "Cubs", "Dbacks", "Dodgers", "Giants", "Guardians",
    # "Mariners", "Mets", "Nationals", "Orioles", "Padres",
    # "Phillies", "Rangers", "Rays", "Reds", "Rockies",
    # "Tigers", "Twins", "Yankees"]

    team_lst = ['yankees']

    # teams_need_work = ['mets',']

    # team_lst_no_data = ['pirates', 'redsox', 'brewers', 
    #                     'marlins', 'whitesox', 'royals']

    for team_name in team_lst: 
        team_name = team_name.lower()
        print(team_name)
        page = requests.get(f'https://www.mlb.com/{team_name}/ballpark/music')
        soup = BeautifulSoup(page.content, 'html.parser')
        # open the file in w mode
        # set encoding to UTF-8
        with open(f'site_output/{team_name}.html', 'w', encoding = 'utf-8') as file:
            # prettify the soup object and convert it into a string
            file.write(str(soup.prettify()))

if __name__ == "__main__":
    main()