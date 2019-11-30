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

class ListboxValuesObs(ListboxValues, Observer):
    def __init__(self, master, validategetcallback=None, regex=None, *args, **kwargs):
        ListboxValues.__init__(self, master, *args, **kwargs)
        Observer.__init__(self)
        self.regex = regex
        self.vgc = validategetcallback

    def update(self, model):

        values = model.get_notewavs(self.regex)
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