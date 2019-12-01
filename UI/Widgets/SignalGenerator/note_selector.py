import subprocess
import sys
import os
import re

from Utils.observer import *
from Generation.frequencies_db_init import *
from Utils.wav_audio import *
from tkinter import Tk, Frame, LabelFrame, StringVar, IntVar, DoubleVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox, Radiobutton, Scale, Entry, messagebox
from tkinter import filedialog
from Utils.signal import *

# TODO: Remove unnecessary import

class NoteSelector(LabelFrame):
    """Note selection widget controller"""

    def __init__(self, parent, *arg, **kwarg):
        super().__init__(parent, *arg, **kwarg)
        self.cursig = None #model is instanciated dynamically

    def _validate_spinbox_octave(self, S, P):
        """[private] validation function of Spinbox widget"""
        if S == '' or P == '': return True
        result = False
        if (S.isdigit()):
            if(int(P)>=2 and int(P)<=5):
                result = True
        if not result: self.bell()
        return result

    def _validate_spinbox_harm(self, S, P):
        """[private] validation function of Spinbox widget"""
        if S == '' or P == '': return True
        result = False
        if (S.isdigit()):
                result = True
        if not result: self.bell()
        return result

    def _validate_freq_entry(self, P):
        if P == '' : return True
        try:
            float(P)
            return True
        except:
            self.bell()
            return False

    def create_UI(self):

        def sharpable(key, checkbox):
            if(key in "BE"):
                checkbox.deselect()
                checkbox.configure(state="disabled")
            else:
                checkbox.configure(state="normal")
            update_selection()

        current_key = StringVar()
        keyvar = StringVar()
        sharpvar = StringVar()
        octave_spin = None
        harmN_spin = None
        note_or_freq = IntVar(0)
        frequency_var = StringVar()
        duration = StringVar()

        def update_selection():
            N_harm = int(harmN_spin.get())
            if(note_or_freq.get() == 0):
                name = keyvar.get() + sharpvar.get() + octave_spin.get()
                freq = getNoteFreq(name)
                duration_time = float(duration.get())
                s = "Selected: {0}".format(name)
                if(freq == -1):
                    s = "frequency not found in db"
                    self.cursig = None
                else:
                    self.cursig = Signal(frequency=freq, N_harm=N_harm, keyname=name, duration=duration_time)
            else:
                freq = float(frequency_var.get())
                duration_time = float(duration.get())
                s = "Selected: {0}Hz".format(freq)
                self.cursig = Signal(frequency=freq, N_harm=N_harm, duration=duration_time)
            current_key.set(s)

        keys = tuple("ABCDEFG")
        keyvar.set(keys[0])
        is_sharp = Checkbutton(self,text="#", variable=sharpvar, onvalue='#', offvalue='',command=update_selection)
        om = OptionMenu(self, keyvar, *keys, command=lambda value=keyvar.get(), checkbox=is_sharp:sharpable(value, checkbox))
        om.grid(row=2, column=1, sticky='w')
        is_sharp.grid(row=2, column=2, sticky='w')

        Label(self, text="Octave 2-5").grid(row=1, column=3)

        vcmd_spinbox = (self.register(self._validate_spinbox_octave), '%S', '%P')
        octave_spin = Spinbox(self, width=10, from_=2, to=5, validate="all",validatecommand=vcmd_spinbox, command=update_selection)
        octave_spin.grid(row=2, column=3, sticky='w')





        frequency_scale = Scale(self, orient="horizontal", from_=0, to=5000, resolution=0.1, tickinterval=1000, length=350, troughcolor="#ABABAB", variable=frequency_var,command=lambda *args:update_selection())
        frequency_scale.grid(row=4, column=1, columnspan=4, sticky='we')
        vcmd_entry = (self.register(self._validate_freq_entry), '%P')
        frequency_entry = Entry(self, textvariable=frequency_var, validate="all", validatecommand=vcmd_entry)
        frequency_entry.grid(row=4, column=5)




        def update_form_disable():
            if(note_or_freq.get()):
                frequency_scale.configure(state="normal", sliderrelief="raised", troughcolor="#ABABAB", showvalue=1)
                frequency_entry.configure(state="normal")
                om.configure(state="disabled")
                is_sharp.configure(state="disabled")
                octave_spin.configure(state="disabled")
            else:
                frequency_scale.configure(state="disabled", sliderrelief="flat", troughcolor="#555555", showvalue=0)
                frequency_entry.configure(state="disabled")
                om.configure(state="normal")
                is_sharp.configure(state="normal")
                octave_spin.configure(state="normal")
            update_selection()

        Radiobutton(self, text="note selection", variable=note_or_freq, value=0, command=update_form_disable).grid(row=2, column=0, sticky='w')
        Radiobutton(self, text="frequence selection", variable=note_or_freq, value=1, command=update_form_disable).grid(row=4, column=0, sticky='w')


        Label(self, text="with").grid(row=5, column=2)
        Label(self, text="harmonics").grid(row=5, column=4)
        vcmd_spinbox_harm = (self.register(self._validate_spinbox_harm), '%S', '%P')
        harmN_spin = Spinbox(self, width=10, from_=0, to=20, validate="all",validatecommand=vcmd_spinbox_harm, command=update_selection)
        harmN_spin.grid(row=5, column=3)



        Label(self, textvariable=current_key, width=20).grid(row=5, column=1)


        Label(self,text="duration (s):").grid(row=6, column=0)
        duration_scale = Scale(self, orient="horizontal", from_=0, to=4, resolution=0.25, tickinterval=1, length=350, digits=3, troughcolor="#ABABAB", variable=duration,command=lambda *args:update_selection())
        duration_scale.grid(row=6, column=1, columnspan=4, sticky='we')
        vcmd_entry = (self.register(self._validate_freq_entry), '%P')
        duration_entry = Entry(self, textvariable=duration, validate="all", validatecommand=vcmd_entry)
        duration_entry.grid(row=6, column=5)



        update_form_disable()
        update_selection()

    def getCurSignal(self):
        if(self.cursig):
            return self.cursig
        return None