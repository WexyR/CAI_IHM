# https://fr.wikipedia.org/wiki/Note_de_musique

import sqlite3
connect = sqlite3.connect("frequencies.db")
cursor = connect.cursor()
cursor.execute("DROP TABLE IF EXISTS frequencies")
cursor.execute("CREATE TABLE frequencies ( \
                    octave INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
                    C float,\
                    CSharp float,\
                    D  float,\
                    DSharp float,\
                    E float,\
                    F float,\
                    FSharp float,\
                    G float,\
                    GSharp float,\
                    A float,\
                    ASharp float,\
                    B float\
);")

def getNoteFreq(note, octave=None, sharp=False):
    assert isinstance(note, str)
    l_note = len(note)
    assert l_note > 0 and l_note <= 3
    assert note[0] in "ABCDEFG"
    if l_note >= 2:
        if "#" in note:
            sharp = True
            note = note.replace('#', '')
        octave = int(note[-1])
        note = note[0]

    if octave is None: raise ValueError("octave can not be None")
    assert isinstance(octave, int)

    return cursor.execute("SELECT {0}{1} FROM frequencies WHERE octave={2};".format(note, ("", "Sharp")[int(sharp)], octave)).fetchone()[0]


f0=440.0
frequencies=[]
octave=[]
octave.append(3)
for j in range (-9,3) :
    frequency=f0*2**(j/12)
    octave.append(frequency)
frequencies.append(octave)

cursor.executemany("INSERT INTO frequencies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", frequencies)
connect.commit()
