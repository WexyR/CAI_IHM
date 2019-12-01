import sys, os
from math import sin,pi
from random import choice
from Utils.observer import *
from Utils.signal import *
from Utils.wav_audio import save_wav
from tkinter import Tk,Canvas, messagebox
from tkinter import filedialog

# TODO: removed unused imports

class Signal(Subject):
    """Signal class"""
    def __init__(self, magnitude=1.0, frequency=1.0, phase=0.0, N_harm=0, duration=2, keyname="", color=None):
        Subject.__init__(self)
        self.set(magnitude, frequency, phase, N_harm, duration, keyname, color)

        self.values = None
        self.wavname = None
        self.isplaying = False

    def __str__(self):
        if self.wavname is None:
            if(self.keyname):
                return self.keyname+".wav"
            return self.get_wavname_by_data()[:-4]
        else:
            return self.wavname

    def set(self, magnitude=1.0, frequency=1.0, phase=0.0, N_harm=0, duration=2, keyname="", color=None):
        self.magnitude = magnitude
        self.frequency = frequency
        self.phase = phase
        self.N_harm = N_harm
        self.duration = duration
        self.keyname = keyname

        if color is None:
            self.color = "#" + "".join([choice("0123456789ABCDEF") for _ in range(6)])
        else:
            self.color = color

    def harmonize(self, t, N=0):
        a,f,p=self.magnitude,self.frequency,self.phase
        return sum([(a/h)*sin(2*pi*(f*h)*t-p) for h in range(1, N+2)])

    def generate(self, period=2, samples=100):
        Tech = period/samples
        print("Tech",Tech,period,samples)
        self.values = [(t*Tech,self.harmonize(t*Tech, self.N_harm)) for t in range(int(samples)+1)]
        print(self)
        self.notify()
        return self.values

    def unset_values(self):
        if(self.values is not None):
            self.values.clear()
            self.notify()

    def generate_sound(self, force=False):
        wavname = self.get_wavname_by_data()

        existing_file = os.path.exists("Sounds/"+wavname)

        print(existing_file)

        if(not force and existing_file):
            self.wavname = wavname
            return 1 #already generated file

        try:
            framerate = 8000
            wav_values = [self.harmonize(t/framerate, self.N_harm) for t in range(int(framerate*self.duration))]
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


    def get_wavname_by_data(self):
        return "{0}_{1:.2f}_{2}_{3}_{4}_{5}.wav".format(self.keyname, self.frequency, self.N_harm, self.duration, self.magnitude, self.phase)

    def reset_wavname(self):
        self.wavname = None
        self.notify()

    def set_wavname(self, name=None):
        if name is None:
            self.wavname = self.get_wavname_by_data()
        else:
            self.wavname = name
        return self.wavname
