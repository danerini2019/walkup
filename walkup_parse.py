import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.mlb.com/phillies/ballpark/music")
soup = BeautifulSoup(page.content, 'html.parser')

stuff = list(soup.children)[1]
lst = [type(item) for item in list(soup.children)]
# print(lst)
stuff = list(stuff.children)[1]
# print(stuff.prettify())
player_names = stuff.find_all(class_="u-text-h4 u-text-flow")
# print(player_names.get_text())
player_songs = stuff.find_all(class_="u-app-show")
# print(player_songs.get_text())

for i in range(len(player_names)):    
    print(player_names[i].get_text())

for i in range(len(player_songs)):    
    print(player_songs[i].get_text())

# Players with multiple songs are separated by returns in 
# the text. Need to pull with conditional statements to
# frame each player