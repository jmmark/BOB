# attempts at pre-processing the lyrics for word-by-word
import re

def load_n_scrub(filename):
    ''' load the corpus of lyrics in filename, scrub of punctuation,
    and return a list of lines with <eol> token at the end '''
    lines = []
    with open(filename, 'r') as f:
        lyrics = f.readlines()
        for line in lyrics:
            line = line.lower()
            line = re.sub(r'[\'\"\[\]().,?!]', '', line)
            line = re.sub(r'\n','', line)
            line = re.sub(r'\s+',' ', line)
            line += ' <eol>'
            lines += [line]

        return(lines)


def overlapping_verses(lines, n):
    '''takes all the individual lines in lines
    and creates n-line verses, overlapping '''
    last_start = len(lines) - n + 1
    verses = []
    for i in range(last_start):
        verse = ' '.join(lines[i:i+n]) + ' <eov>'
        verses += [verse]

    return(verses)

def non_overlapping_verses(lines, n):
    '''takes all the individual lines in lines
    and creates n-line verses, overlapping '''
    last_start = len(lines) - n + 1
    verses = []
    for i in range(0, last_start, n):
        verse = ' '.join(lines[i:i+n]) + ' <eov>'
        verses += [verse]

    return(verses)

if __name__ == "__main__":
    lines = load_n_scrub('all_gbv_lyrics.txt')
    verses = non_overlapping_verses(lines, 4)
    print('\n'.join(lines[:8]))
    print('\n'.join(verses[:2]))
