import subprocess
import sys
import os
import re

from Utils.observer import Subject, Observer
from Utils.wav_audio import *

from UI.Widgets.SignalListbox.listbox_values import *

from Generation.frequencies_db_init import *

from tkinter import Tk, Frame, LabelFrame, StringVar, IntVar, DoubleVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox, Radiobutton, Scale, Entry, messagebox
from tkinter import filedialog

# TODO: Remove unnecessary import

class ListboxValuesObs(ListboxValues, Observer):

    def __init__(self, master, validategetcallback=None, dirpath=None, regex=None, *args, **kwargs):

        ListboxValues.__init__(self, master, *args, **kwargs)
        Observer.__init__(self)
        self.regex = regex
        self.dirpath = dirpath
        self.vgc = validategetcallback
        self.valuemode = valuemode

    def update(self, model):

        values = dict()
        note_values, chord_values = model.get_wavs(self.dirpath, self.regex)
        values.update(note_values)
        values.update(chord_values)

        l_values = self.get(0, self.size()-1)

        # index_of_deleted_val = sorted([ind for ind, val in l_values if val not in values])
        # index_of_deleted_val = [v-l2.index(v) for v in index_of_deleted_val]
        # for ind in index_of_deleted_val:
        #     self.delete(ind)

        for path, signal in values.items():
            print(path)
            if self.vgc is not None:
                if not self.vgc((path, signal)):
                    continue
            if(path[1] not in [signame for signame, sig in self.get(0, self.size()-1)]):
                self.insert(0, signal)
