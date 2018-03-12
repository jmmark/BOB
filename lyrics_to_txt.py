# write all the lyrics of all songs out as a text file for further processing
import sqlite3

db_file = "GBV_Lyrics.db"
txt_file = "all_gbv_lyrics.txt"

sql_command = """ SELECT line FROM lyrics """

conn = sqlite3.connect(db_file)
c = conn.cursor()

all_lines = c.execute(sql_command).fetchall()

with open(txt_file, "w") as f:
    for l in all_lines:
        try:
            f.write(l[0] + '\n')
        except:
            print(l[0], 'could not be written')


conn.close()