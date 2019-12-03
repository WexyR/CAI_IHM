import subprocess
import sys
import os
import re

from Utils.signal import *
from Utils.chord import *
from Utils.observer import Subject, Observer
from Generation.frequencies_db_init import *
from Utils.wav_audio import *
from tkinter import Tk, Frame, LabelFrame, StringVar, IntVar, DoubleVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox, Radiobutton, Scale, Entry, messagebox
from tkinter import filedialog

# TODO: Remove unnecessary import

class SignalsModel(Subject):
    """model, represent the list of all wav signal"""

    def __init__(self, inner_views=[], paths=["Sounds/", "Sounds/Chords"]):
        super().__init__()
        if not isinstance(inner_views, list):
            print("/!\\warning/!\\, depreciation: inner_views arguments is not a list. Automatically converted to list")
            inner_views = list(inner_views)

        self.note_wavs = {}
        self.chord_wavs = {}
        self.inner_views = inner_views
        self.paths = paths

    def strinfo_to_infodict(self, strinfo):
        """decompile signal info in strinfo"""
        dot = strinfo.find('.wav')
        if(dot != -1):
            strinfo = strinfo[:dot]
        info = strinfo.split('_')
        info_dict = dict()
        if(re.match("[A-G]#?[0-9]", info[0])):
            info_dict["keyname"] = info[0]


        if(len(info) == 6):
            info_dict["frequency"] = float(info[1])
            info_dict["N_harm"] = int(float(info[2]))
            info_dict["duration"] = float(info[3])
            info_dict["magnitude"] = float(info[4])
            info_dict["phase"] = float(info[5])
        else:
            if("keyname" in info_dict.keys()):
                info_dict["frequency"] = getNoteFreq(info_dict["keyname"])
            else:
                return None
        return info_dict

    def update_data(self):
        l_dir = []
        for path in self.paths:
            l_dir += [(path,file_name) for file_name in os.listdir(path) if os.path.isfile(path + file_name) and file_name[-3:]=="wav"]

        # check deleted note wav file
        for key in self.note_wavs.keys():
            if(len(key[1].split('~')) != 1): #chord
                continue
            if(key[1].split("_")[0] == ""): #doesn't need wav
                continue
            if(key not in l_dir): # file deleted
                del self.note_wavs[key]

        # check deleted note wav file
        to_remove=[]
        for key in self.chord_wavs.keys():
            if(len(key[1].split('~')) == 1): #note
                continue
            if(key not in l_dir): # file deleted
                del self.chord_wavs[key]

        # TODO: Have it work pls :(



        for key in l_dir:
            if(len(key[1].split('~')) == 1):
                if(key not in self.note_wavs.keys()):
                    sig_parameters = self.strinfo_to_infodict(key[1])
                    if sig_parameters is None:
                        print("unable to decompile the file {0}{1}".format(*key))
                        continue

                    s = Signal(**sig_parameters)
                    s.set_wavname(key[1])
                    for view in self.inner_views:
                        s.attach(view)
                    self.note_wavs[key] = s
            else:
                if(key not in self.note_wavs.keys()):
                    sig_infos = key[1].split('~')
                    sigs = []
                    for sig_info in sig_infos:
                        sig_parameters = self.strinfo_to_infodict(sig_info)
                        if sig_parameters is None:
                            print("unable to decompile the file {0}{1}".format(*key))
                            break
                        sigs.append(Signal(**sig_parameters))
                    chord = Chord(signals=sigs)
                    chord.set_wavname(key[1])
                    for view in self.inner_views:
                        chord.attach(view)
                    self.chord_wavs[key] = chord



        self.notify()

    def register_signal(self, signal, path=""):
        keyname = signal.get_wavname_by_data()
        if((path, keyname) in self.note_wavs.keys()):
            messagebox.showwarning("Already existing signal", "This signal is already existing. Aborting creation.")
            return -1

        self.note_wavs[(path, keyname)] = signal

    def get_wavs(self, dirpath=None, regex=None):
        """return all note which have a match with the regular_expression in the name"""
        if dirpath is None and regex is None:
            return self.note_wavs, self.chord_wavs
        else:
            note_result=dict()
            chord_result=dict()
            for fullpath, sig in self.note_wavs.items():

                dpath, file_name = fullpath
                if(dirpath is not None):
                    if dpath not in dirpath:
                        continue
                if(regex is not None):
                    if not re.match(regex, file_name):
                        continue
                note_result[fullpath] = sig

            for fullpath, chord in self.chord_wavs.items():

                dpath, file_name = fullpath
                if(dirpath is not None):
                    if dpath not in dirpath:
                        continue
                if(regex is not None):
                    if not re.match(regex, file_name):
                        continue
                chord_result[fullpath] = chord


            return note_result, chord_result
