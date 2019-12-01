import subprocess
import sys
import os
import re

from Utils.observer import Subject, Observer
from Generation.frequencies_db_init import *
from Utils.wav_audio import *
from tkinter import Tk, Frame, LabelFrame, StringVar, IntVar, DoubleVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox, Radiobutton, Scale, Entry, messagebox
from tkinter import filedialog

# TODO: Remove unnecessary import

class ListboxValues(Listbox):
    """Listbox widget but also save variables in a list (not just the __str__ value)"""
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.values = []

    def insert(self, *arg, **kwargs):
        super().insert(*arg, **kwargs)
        self.values.insert(*arg, **kwargs)

    def get(self, start, end=None):
        if not isinstance(start, int): raise TypeError("start must be integer")
        if not isinstance(end, int) and end is not None: raise TypeError("end must be integer or None")
        names = super().get(start, end)
        if end is not None:
            return [(names[i], self.values[i]) for i in range(start,end+1)]
        else:
            return (names, self.values[start])

    def delete(self, start, end=None):
        if not isinstance(start, int): raise TypeError("start must be integer")
        if not isinstance(end, int) and end is not None: raise TypeError("end must be integer or None")

        if end is not None:
            for i in range(start, end+1):
                del self.values[start]
        else:
            del self.values[start]

        super().delete(start, end)
