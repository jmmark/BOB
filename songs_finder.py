import config
import requests
import sqlite3
from sqlite3 import Error

'''Get GBV songs and urls from Genius.  Create the SQLlite database if necessary and 
add the tables.  Then record the songs'''

def create_connection(db_file):
    '''create database connection.  Should create db if it doesn't exist'''
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    '''create a table in conn according to create_table_sql'''
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_song(conn, song):
    '''insert a song, provided it doesnt already exist'''
    sql_command = ''' INSERT OR IGNORE INTO songs(id, title, url)
                        VALUES(?,?,?) '''

    c = conn.cursor()
    c.execute(sql_command, song)

    print(c.lastrowid)



db = 'GBV_Lyrics.db'

create_songs_table = ''' CREATE TABLE IF NOT EXISTS songs (
                            id integer PRIMARY KEY,
                            title text NOT NULL,
                            url text NOT NULL,
                            scraped boolean DEFAULT false
                            );'''

create_lyrics_table = ''' CREATE TABLE IF NOT EXISTS lyrics (
                            line_id integer PRIMARY KEY,
                            song_id integer,
                            line text,
                            FOREIGN KEY (song_id) REFERENCES songs (id)
                            );'''

from bs4 import BeautifulSoup

# set up the db connections and create the tables if necessary
conn = create_connection(db)
create_table(conn, create_songs_table)
create_table(conn, create_lyrics_table)


base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer ' + config.bearer_token}
artist_id = 28684
search_url = base_url + "/artists/28684/songs"

# can only get 50 responses per page
counter = 1
valid = True
while valid:
    data = {'per_page': 50, 'page':counter}
    response = requests.get(search_url, params=data, headers=headers)
    json = response.json()

    if (json['meta']['status'] != 200 or not json['response']['songs']):
        valid = False
        continue
    #print(headers)
    #print(json)
    #print(response.url)
    #song_info = None
    for song in json["response"]["songs"]:
        print(song["title"])#, type(song["id"]))
        song_tbl = (song["id"], song["title"], song["url"])
        insert_song(conn, song_tbl)


    counter += 1

conn.commit()
conn.close()