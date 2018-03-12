import config
import requests
import sqlite3
from bs4 import BeautifulSoup

db = "GBV_Lyrics.db"

conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("SELECT * FROM songs WHERE scraped = 'false'")
unscrubbed = c.fetchall()
#unscrubbed = [c.fetchone()] #one at a time for testing


def write_lyrics(conn, line):
    '''write the song id and line to the lyrics table
    primary key will take care of itself as sequential'''
    sql_command = '''INSERT INTO lyrics (song_id, line) 
                    VALUES (?,?) '''

    c = conn.cursor()
    c.execute(sql_command, line)

def update_as_scraped(conn, song_id):
    ''' mark the song as scraped so it need not do it again '''
    sql_command = ''' UPDATE songs 
                    SET scraped = ? 
                    WHERE id = ? '''

    c = conn.cursor()
    c.execute(sql_command, ('true', song_id))


#print(unscrubbed[0])
def lyrics_scraper(url):
    '''scrape lyrics from genius page specified by url'''
    lyrics_page = requests.get(url)
    html = BeautifulSoup(lyrics_page.text, 'html.parser')
    lyrics = html.find('div', class_="lyrics").get_text()
    return lyrics

for song in unscrubbed:
    # first parse the lyrics into a list of lines, removing comments
    print(song[1])
    lyr = lyrics_scraper(song[2]).strip().split("\n")
    lyr = [x for x in lyr if x != '']
    lyr = [x for x in lyr if x[0] != '[']

    # now write the lines to lyrics
    for l in lyr:
        write_lyrics(conn, (song[0], l))


    # now mark the song as scrubbed
    update_as_scraped(conn, song[0])
    conn.commit()


#print([x for x in lyr.strip().split("\n") if x[0] != "["])
conn.close()
