# -*- coding: utf-8 -*-
# script wav_audio.py
#http://fsincere.free.fr/isn/python/cours_python_ch9.php
#http://izeunetit.fr/ICN1ere/son_audio.php
# (C) Fabrice Sincère ; Jean-Claude Meilland

import wave
import math
import os
import threading

import sqlite3
import Generation.frequencies_db_init

## Création d'un fichier audio au format WAV (PCM 8 bits stéréo 44100 Hz)
## Son de forme sinusoïdale sur chaque canal

def create_note_wav(degree,name,left_frequency,right_frequency) :
    global ioMutex
    if type(degree) != str :
        degree=str(degree)
    file= "Sounds/"+name+degree+".wav"
    sound=wave.open(file,'w')
    nb_channels = 2    # stéreo
    nb_bytes = 1       # taille d'un échantillon : 1 octet = 8 bits
    sampling = 44100   # fréquence d'échantillonnage
    left_level = 1     # niveau canal de gauche (0 à 1) ? '))
    right_level= 1    # niveau canal de droite (0 à 1) ? '))
    duration = 1
    nb_samples = int(duration*sampling)
    params = (nb_channels,nb_bytes,sampling,nb_samples,'NONE','not compressed')

    sound.setparams(params)    # création de l'en-tête (44 octets)

    # niveau max dans l'onde positive : +1 -> 255 (0xFF)
    # niveau max dans l'onde négative : -1 ->   0 (0x00)
    # niveau sonore nul :                0 -> 127.5 (0x80 en valeur arrondi)

    left_magnitude = 127.5*left_level
    right_magnitude= 127.5*right_level

    values = []
    for i in range(0,nb_samples):
        k=min(1,5*i/sampling)*min(1,5*(nb_samples-i)/sampling)
        # canal gauche
        # 127.5 + 0.5 pour arrondir à l'entier le plus proche
        left_value = wave.struct.pack('B',int(128.0 + k*left_magnitude*math.sin(2.0*math.pi*left_frequency*i/sampling)))
        # canal droit
        right_value = wave.struct.pack('B',int(128.0 + k*right_magnitude*math.sin(2.0*math.pi*right_frequency*i/sampling)))
        values.append(left_value)
        values.append(right_value)
    value_str = b''.join(values)
    ioMutex.acquire() # By doing that we ensure there is only one thread writing at a time. It should improve performance.
    sound.writeframes(value_str)
    ioMutex.release()
    sound.close()

def generate():
    connect = sqlite3.connect("Generation/frequencies.db")
    cursor = connect.cursor()
    gammes=cursor.execute("SELECT * FROM frequencies").fetchall()
    notes=["octave","C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    n_note = cursor.execute("SELECT COUNT(*) FROM frequencies").fetchone()[0]*(len(notes)-1)
    j=0
    threads = []
    print("Generating wav files from frequencies db...")
    for gamme in gammes :
        for i in range(1,len(gamme)) :
            j+=1
            if not os.path.exists("Sounds/"+notes[i]+str(gamme[0])+".wav"):
                print("Generating {0}/{1} (Sounds/{2}.wav)".format(j, n_note, notes[i]+str(gamme[0])))
                threads.append(threading.Thread(target=create_note_wav, args=(gamme[0],notes[i],gamme[i],2*gamme[i])))
                threads[-1].start()
    for thread in threads :
        thread.join()
    print("Done loading {0} sounds!".format(n_note))

ioMutex = threading.Lock()
generate()
