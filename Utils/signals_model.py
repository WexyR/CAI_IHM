import subprocess
import sys
import os
import re

from UI.frequencies_viewer import View, Signal
from observer import Subject, Observer
from Generation.frequencies_db_init import *
from Utils.wav_audio import *
from tkinter import Tk, Frame, LabelFrame, StringVar, IntVar, DoubleVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox, Radiobutton, Scale, Entry, messagebox
from tkinter import filedialog

# TODO: Remove unnecessary import

class SignalsModel(Subject):
    """model, represent the list of all wav signal"""

    def __init__(self, inner_views=[]):
        super().__init__()
        if not isinstance(inner_views, list):
            print("/!\\warning/!\\, depreciation: inner_views arguments is not a list. Automatically converted to list")
            inner_views = list(inner_views)

        self.note_wavs = {}
        self.chord_wav = {}
        self.inner_views = inner_views

    def update_note_data(self, paths=["Sounds/"]):
        l_dir = []
        for path in paths:
            l_dir += [(path,file_name) for file_name in os.listdir(path) if os.path.isfile(path + file_name) and file_name[-3:]=="wav"]


        for key in self.note_wavs.keys():
            if(key[1].split("_")[0] == ""): #doesn't need wav
                continue
            if(key not in l_dir): # file deleted
                del self.note_wavs[key]

        # keys = self.note_wavs.keys()
        for key in l_dir:
            if(key not in self.note_wavs.keys()):
                info = key[1][:-4].split("_")
                # print(info)
                # try:
                keyname = info[0]
                if(keyname == "chord"):
                    continue
                if(len(info)>1):
                    freq = float(info[1])
                    s_index = info[3].find("s")
                    if s_index:
                        info[3] = info[3][:s_index]
                    duration = float(info[3])
                    N_harm = int(float(info[2]))
                else:
                    # print(keynae)
                    freq = getNoteFreq(keyname)
                    N_harm = 1
                    duration = 2
                # except Exception as e:
                #     print(e)
                #     continue

                s = Signal(frequency=freq, N_harm=N_harm, duration=duration, keyname=keyname)
                s.set_wavname()
                for view in self.inner_views:
                    print(view)
                    s.attach(view)
                self.note_wavs[key] = s
        self.notify()

    def register_signal(self, signal, path=""):
        keyname = signal.get_wavname_by_data()
        if((path, keyname) in self.note_wavs.keys()):
            messagebox.showwarning("Already existing signal", "This signal is already existing. Aborting creation.")
            return -1

        self.note_wavs[(path, keyname)] = signal




    def get_notewavs(self, regular_expression=None):
        """return all note which have a match with the regular_expression in the name"""
        if regular_expression is None:
            return self.note_wavs
        else:
            pass
            # TODO: return with regex
            # return set([elem for elem in self.wavs if re.match(regular_expression,elem.wavname)])

    def get_chordwavs(self, regular_expression=None):
        """return all chords which have a match with the regular_expression in the name"""
        if regular_expression is None:
            return self.note_wavs
        else:
            pass
            # TODO: return with regex
            # return set([elem for elem in self.wavs if re.match(regular_expression,elem.wavname)])
