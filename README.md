This project aims to parse, clean, model, and analyze MLB walkup songs from the official MLB website

 Next steps (no order):
 - split song column into artist and song columns - Done
 - extrapolate logic to all teams - probably just call GET in loop or list of teams
    - Added looping for each team. There are different html layouts for many teams so I need to adapt the parsing for every scenario. still figureing this out - Done
 - website includes spotify link to song, can use this rather than spotify API?
 - add year and team columns - Done

 Potential Analysis routes:
 - spotify connection to determine characteristics of walkup songs
    - hype factor
    - genres
    - how indie? fewest listens
 - connection to baseball library to get stats of different players by genre
    - slumping players changing their song more often
    - what genre/artist had the best/worst stats



