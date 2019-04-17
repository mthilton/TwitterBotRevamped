# TwitterBotRevamped
Takes current user listening data and creates and tweets out the song, artist, and song link.   

## Required Libraries
- Spotipy
- Python-Twitter
- Mysql Connector

## Upcoming Features
- (REVERTED) Instead of just having the artists' name, use their twitter handle so they have a direct link.
- (COMPLETED!) Create a database of songs listened to so we can have like a weekly top hits playlist created and tweeted out.

## Changelog
- 4/2/2019
   - Been working a lot on the database aspect of things and cleaning up the app code itself.
   - *NEW* Now have two playlists: one containing my alltime most listened to songs starting in March of 2019
           and one containing my most listened to songs of that week. They can be found here: [Weekly](https://open.spotify.com/user/12140121901/playlist/2mSILmJCJE6dIAU8GJuuho?si=sJxs9lmZS_SAgX8yYpww-A, "Matt's Weekly Hits") & [Alltime](https://open.spotify.com/user/12140121901/playlist/4SPUd4E1c6Iam2cWKeub7y?si=r9rKJEu1RpCGq_5jfOBMbg, "Matt's Alltime Hits")
   - Bugfixes... Many bug fixes...        

- 1/5/2019
   - Reverting previous changes, linked too many incorrect accounts

- 1/4/2019
   - *NEW* If the artist has a verified twitter account, the bot will now link the artists' account as well (For now the query is limited to the first 5 results from twitter) (Sorry unverified artists :( )

- 1/3/2019
   - Completed the main Function of the bot. It has been temporarily deployed. Will need to move it to a dedicated server

- 1/2/2019
   - Initial Commit
