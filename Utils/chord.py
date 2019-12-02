import sys, os
from math import sin,pi
from random import choice
from Utils.observer import *
from Utils.signal import *
from Utils.wav_audio import save_wav
from tkinter import Tk,Canvas, messagebox
from tkinter import filedialog

# TODO: removed unused imports

class Chord(Subject):
    """Chord class"""
    def __init__(self, signals=[], color=None):
        Subject.__init__(self)

        self.set(signals)
        self.signals.sort(key=lambda x: x.wavname)

        self.values = None
        self.wavname = None
        self.isplaying = False

    def __str__(self):
        return "|".join([str(s)[:-4] for s in self.signals])+".wav"

    def set(self, signals=[]):
        self.signals = signals
        self.duration = max([s.duration for s in self.signals])

    def generate(self, period=2, samples=100):
        Tech = period/samples
        self.values = [(t*Tech,sum([s.harmonize(t*Tech, s.N_harm) for s in self.signals])) for t in range(int(samples)+1)]
        print(self)
        self.notify()
        return self.values

    def unset_values(self):
        if(self.values is not None):
            self.values.clear()
            self.notify()

    def generate_sound(self, force=False):
        wavname = self.__str__()

        existing_file = os.path.exists("Sounds/Chords/"+wavname)

        print(existing_file)

        if(not force and existing_file):
            self.wavname = wavname
            return 1 #already generated file

        try:
            framerate = 8000
            wav_values = [(sum([s.harmonize(t/framerate, s.N_harm) if t<s.duration else 0 for s in self.signals])/len(self.signals)) for t in range(int(framerate*self.duration))]
            save_wav(wavname, wav_values, framerate)


            success = True
        except Exception as e:
            print(e)
            success = False

        if(success):
            self.wavname = wavname
            return 0 #sucess
        else:
            return -1 #error

    def play(self):
        if self.wavname is not None:
            self.isplaying = True
            self.notify()
            self.isplaying = False
            return 0
        else:
            return -1

    #def get_wavname_by_data(self):
    #    return "{0}_{1:.2f}_{2}_{3}_{4}_{5}.wav".format(self.keyname, self.frequency, self.N_harm, self.duration, self.magnitude, self.phase)

    #def reset_wavname(self):
    #    self.wavname = None
    #    self.notify()

    #def set_wavname(self, name=None):
    #    if name is None:
    #        self.wavname = self.get_wavname_by_data()
    #    else:
    #        self.wavname = name
    #    return self.wavname
