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

class Speaker(Observer):
    def __init__(self):
        super().__init__()

    def update(self, sig):
        print(sig)
        if(sig.isplaying):
            if(os.path.exists("Sounds/"+sig.wavname)):
                print("test")
                subprocess.call(["aplay", "Sounds/"+sig.wavname])
