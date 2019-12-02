import subprocess
import sys
import os
import re

from Utils.signal import *
from Utils.observer import Subject, Observer
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
        self.chord_wavs = {}
        self.inner_views = inner_views

    def strinfo_to_infodict(self, strinfo):
        """decompile signal info in strinfo"""
        dot = strinfo.find('.wav')
        if(dot != -1):
            strinfo = strinfo[:dot]
        info = strinfo.split('_')
        print(info, len(info))
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

    def update_note_data(self, paths=["Sounds/"]):
        l_dir = []
        for path in paths:
            l_dir += [(path,file_name) for file_name in os.listdir(path) if os.path.isfile(path + file_name) and file_name[-3:]=="wav"]

        # check deleted note wav file
        for key in self.note_wavs.keys():
            if(len(key[1].split('|')) != 1): #chord
                continue
            if(key[1].split("_")[0] == ""): #doesn't need wav
                continue
            if(key not in l_dir): # file deleted
                del self.note_wavs[key]

        # check deleted note wav file
        for key in self.chord_wavs.keys():
            if(len(key[1].split('|')) == 1): #note
                continue
            if(key not in l_dir): # file deleted
                del self.chord_wavs[key]





        for key in l_dir:
            if(len(key[1].split('|')) == 1):
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
                    sig_infos = [sig.split('_') for sig in key[1].split('|')]
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
                        s.attach(view)
                    self.chord_wavs[key] = s



        self.notify()

    def register_signal(self, signal, path=""):
        keyname = signal.get_wavname_by_data()
        if((path, keyname) in self.note_wavs.keys()):
            messagebox.showwarning("Already existing signal", "This signal is already existing. Aborting creation.")
            return -1

        self.note_wavs[(path, keyname)] = signal

    def get_notewavs(self, dirpath=None, regex=None):
        """return all note which have a match with the regular_expression in the name"""
        if regex is None:
            return self.note_wavs
        else:
            result=dict()
            for fullpath, sig in self.note_wavs.items():

                dpath, file_name = fullpath
                if dpath != dirpath:
                    continue
                if not re.match(regex, file_name):
                    continue
                result[fullpath] = sig
            return result

    def get_chordwavs(self, regular_expression=None):
        """return all chords which have a match with the regular_expression in the name"""
        if regular_expression is None:
            return self.note_wavs
        else:
            pass
            # TODO: return with regex
            # return set([elem for elem in self.wavs if re.match(regular_expression,elem.wavname)])

    # def execute_on_sigs(self, regular_expression, callback, *cbargs, **cbkwargs):
    #     sigs = self.get_notewavs(dirpath, file_name).values()
    #     print(sigs)
    #     for sig in sigs:
    #         callback(sig, *cbargs, **cbkwargs)
