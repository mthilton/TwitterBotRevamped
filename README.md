# TwitterBotRevamped

Let's people know what I'm listening to on Spotify. The app.py file watches my spotify and updates a database with all of my listening data. Then playlist_update.py will promote playlists that represent what I have been listening to.

Current playlists:

1. [Matt's Weekly Hits](https://open.spotify.com/user/12140121901/playlist/2mSILmJCJE6dIAU8GJuuho?si=sJxs9lmZS_SAgX8yYpww-A, "Matt's Weekly Hits")
2. [Matt's Alltime Hits](https://open.spotify.com/user/12140121901/playlist/4SPUd4E1c6Iam2cWKeub7y?si=r9rKJEu1RpCGq_5jfOBMbg, "Matt's Alltime Hits")
3. [Top Artists, Top Tracks](https://open.spotify.com/playlist/09JEGNffReWWKxbARkcj75?si=Xby_9PJpSxmZNAkW6kA7_Q, "Top Artists, Top Tracks")
4. [Hipsters Paridise](https://open.spotify.com/playlist/57b8JKq3G9BG7IEuphgjD0?si=ysJ6hAZUR4GATYF4zZQhPA, "Hipsters Paridise")
5. ~~[Every Song I have Ever Listened To*](https://open.spotify.com/playlist/404, "Broken, Listen at your own discretion")~~

## Required Libraries

- Spotipy
- Python-Twitter
- Mysql Connector

## Upcomming Features

- [ ] Detection and tweeting of "Hot Items." If they are on repeat, the pepole should know that im really into what I'm listening to.
    - Here are the items that can be "Hot":
        - [ ] Track
        - [ ] Artist
        - [ ] Album
        - [ ] Playlist
- [x] More playlists! Added Top Artists, Top Tracks and Hipsters Paridise
- [x] Create a database of songs listened to so we can have like a weekly top hits playlist created and tweeted out.
- [ ] ~~Instead of just having the artists' name, use their twitter handle so they have a direct link.~~ (Canceled)

## Changelog

- 4/3/2021
    - [*Depricated*] The deprication code file has been... depricated. It didn't make any sense to have since git is literal version control. If I need the code, I can go back and get it.
    - [*NEW*] New Playlists have finally been implemented: Top Artists, Top Tracks and Hipsters Paridise
    - Refractor and removed a lot of code that was either unneccisary or redundant.
    - Updated the readme

- 5/2/2021
    - Removed tweet related code from the active listener. Realized that nobody really cared what I was actively listening to. However, playlists are things people care about.
    - Updated the readme
    - [*NEW*] depricaded code file for greater functions that have been removed. Just in case :)

- 4/2/2019
    - Been working a lot on the database aspect of things and cleaning up the app code itself.
    - [*NEW*] Now have two playlists: one containing my alltime most listened to songs starting in March of 2019
              and one containing my most listened to songs of that week. They can be found here: [Weekly](https://open.spotify.com/user/12140121901/playlist/2mSILmJCJE6dIAU8GJuuho?si=sJxs9lmZS_SAgX8yYpww-A, "Matt's Weekly Hits") & [Alltime](https://open.spotify.com/user/12140121901/playlist/4SPUd4E1c6Iam2cWKeub7y?si=r9rKJEu1RpCGq_5jfOBMbg, "Matt's Alltime Hits")
    - Bugfixes... Many bug fixes...

- 1/5/2019
    - Reverting previous changes, linked too many incorrect accounts

- 1/4/2019
    - [*NEW*] If the artist has a verified twitter account, the bot will now link the artists' account as well (For now the query is limited to the first 5 results from twitter) (Sorry unverified artists :( )

- 1/3/2019
    - Completed the main Function of the bot. It has been temporarily deployed. Will need to move it to a dedicated server

- 1/2/2019
    - Initial Commit
