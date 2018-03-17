# write all the lyrics of all songs out as a text file for further processing
import sqlite3

def scrub_windows(txt):
    '''there are some rogue windows-1252 characters in tere.'''
    windows_chars = {b'\x91'.decode('windows-1252'):"'",
                     b'\x92'.decode('windows-1252'):"'",
                     b'\x93'.decode('windows-1252'): '"',
                     b'\x94'.decode('windows-1252'): '"',
                     b'\x85'.decode('windows-1252'): "...",
                     b'\xe8'.decode('windows-1252'): "e",
                     b'\xb0'.decode('windows-1252'): " degrees"
                     }

    clean_txt = txt
    for wc, uc in windows_chars.items():
        clean_txt = clean_txt.replace(wc, uc)

    return clean_txt

db_file = "GBV_Lyrics.db"
txt_file = "all_gbv_lyrics.txt"

sql_command = """ SELECT line FROM lyrics """

conn = sqlite3.connect(db_file)
c = conn.cursor()

all_lines = c.execute(sql_command).fetchall()

with open(txt_file, "w") as f:
    for l in all_lines:
        try:

            fixed_encoding = scrub_windows(l[0])

            f.write(fixed_encoding + '\n')
        except:
            print(l[0], 'could not be written')


conn.close()