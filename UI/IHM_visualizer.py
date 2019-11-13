from UI.frequencies_viewer import View, Signal
from observer import Subject, Observer
from Generation.frequencies_db_init import *

import sys
if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import Tk,Frame, StringVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import Tk,Frame,StringVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox
    from tkinter import filedialog




class NoteSelector(Frame):
    """Note selection widget controller"""

    def __init__(self, parent, model=None, *arg, **kwarg):
        super().__init__(parent, *arg, **kwarg)
        self.model = model

    def _validate_spinbox_octave(self, S, P):
        """[private] validation function of Spinbox widget"""
        if S == '' or P == '': return True
        result = False
        if (S.isdigit()):
            if(int(P)>=2 and int(P)<=5):
                result = True
        return result
    def _validate_spinbox_harm(self, S, P):
        """[private] validation function of Spinbox widget"""
        if S == '' or P == '': return True
        result = False
        if (S.isdigit()):
                result = True
        return result

    def create_UI(self):

        def sharpable(key, checkbox):
            if(key in "BE"):
                checkbox.deselect()
                checkbox.configure(state="disabled")
            else:
                checkbox.configure(state="normal")


        keys = tuple("ABCDEFG")
        keyvar = StringVar()
        keyvar.set(keys[0])
        sharpvar = StringVar()
        is_sharp = Checkbutton(self,text="#", variable=sharpvar, onvalue='#', offvalue='')
        om = OptionMenu(self, keyvar, *keys, command=lambda value=keyvar.get(), checkbox=is_sharp:sharpable(value, checkbox))
        om.grid(row=2, column=1)
        is_sharp.grid(row=2, column=2)

        Label(self, text="Octave 2-5").grid(row=1, column=3)

        vcmd_spinbox = (self.register(self._validate_spinbox_octave), '%S', '%P')
        octave = Spinbox(self, from_=2, to=5, validate="all",validatecommand=vcmd_spinbox)
        octave.grid(row=2, column=3)

        Label(self, text="N Harmoniques").grid(row=1, column=4)
        vcmd_spinbox_harm = (self.register(self._validate_spinbox_harm), '%S', '%P')
        harmN = Spinbox(self, from_=0, to=20, validate="all",validatecommand=vcmd_spinbox_harm)
        harmN.grid(row=2, column=4)

        registered_keys = Listbox(self)
        registered_keys.grid(row=3, column=1)
        def delete_key(event):
            indexes = registered_keys.curselection()
            if(indexes): registered_keys.delete(*indexes)
            self.model.values = None
            self.model.notify()
        def insert_key(event=None):
            name = keyvar.get() + sharpvar.get() + octave.get()
            freq = getNoteFreq(name)
            registered_keys.insert(0,name)
            self.model.set(name, 1, freq, N_harm=int(harmN.get()))
            self.model.generate()
        registered_keys.bind("<BackSpace>", delete_key)
        Button(self, text="test", command=insert_key).grid(row=2, column=5)
