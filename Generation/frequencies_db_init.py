# https://fr.wikipedia.org/wiki/Note_de_musique

import sqlite3
import os

def loadOctave(f0, index):
    frequencies=[]
    octave=[]
    octave.append(index)
    for j in range (-9,3) :
        frequency=f0*2**(j/12)
        octave.append(frequency)
    frequencies.append(octave)

    cursor.executemany("INSERT INTO frequencies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", frequencies)
    connect.commit()

if not os.path.exists("Generation/frequencies.db"):
    connect = sqlite3.connect("Generation/frequencies.db")
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
                        A      float,\
                        ASharp float,\
                        B float\
    );")

    print("Generating octave tables...")
    n_octave = 4
    for i in range(0,n_octave):
        loadOctave(440.0*2**(i-3), i)
    print("Done generating tables!")
