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

class ListboxValues(Listbox):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.values = []

    def insert(self, *arg, **kwargs):
        super().insert(*arg, **kwargs)
        self.values.insert(*arg, **kwargs)

    def get(self, start, end=None):
        print((start, end))
        if not isinstance(start, int): raise TypeError("start must be integer")
        if not isinstance(end, int) and end is not None: raise TypeError("end must be integer or None")
        names = super().get(start, end)
        if end is not None:
            return [(names[i], self.values[i]) for i in range(start,end+1)]
        else:
            return (names, self.values[start])

    def delete(self, start, end=None):
        print((start, end))
        if not isinstance(start, int): raise TypeError("start must be integer")
        if not isinstance(end, int) and end is not None: raise TypeError("end must be integer or None")
        super().delete(start, end)
        if end is not None:
            for i in range(start, end):
                del self.values[i]
        else:
            del self.values[start]



class NoteSelector(Frame):
    """Note selection widget controller"""

    def __init__(self, parent, *arg, **kwarg):
        super().__init__(parent, *arg, **kwarg)
        self.cursig = None

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

        def update_selection():
            name = keyvar.get() + sharpvar.get() + octave_spin.get()
            freq = getNoteFreq(name)
            N_harm = int(harmN_spin.get())
            s = "Selected: {0} ; N={1}".format(name, N_harm)
            current_key.set(s)
            self.cursig = Signal(frequency=freq, N_harm=N_harm, keyname=name)

        keys = tuple("ABCDEFG")
        keyvar.set(keys[0])
        is_sharp = Checkbutton(self,text="#", variable=sharpvar, onvalue='#', offvalue='',command=update_selection)
        om = OptionMenu(self, keyvar, *keys, command=lambda value=keyvar.get(), checkbox=is_sharp:sharpable(value, checkbox))
        om.grid(row=2, column=1)
        is_sharp.grid(row=2, column=2)

        Label(self, text="Octave 2-5").grid(row=1, column=3)

        vcmd_spinbox = (self.register(self._validate_spinbox_octave), '%S', '%P')
        octave_spin = Spinbox(self, from_=2, to=5, validate="all",validatecommand=vcmd_spinbox, command=update_selection)
        octave_spin.grid(row=2, column=3)

        Label(self, text="N Harmoniques").grid(row=1, column=4)
        vcmd_spinbox_harm = (self.register(self._validate_spinbox_harm), '%S', '%P')
        harmN_spin = Spinbox(self, from_=0, to=20, validate="all",validatecommand=vcmd_spinbox_harm, command=update_selection)
        harmN_spin.grid(row=2, column=4)


        Label(self, textvariable=current_key).grid(row=2, column=5)
        update_selection()
        # Button(self, text="Valider", command=submit).grid(row=2, column=5)

    def getCurSignal(self):
        if(self.cursig):
            return self.cursig
        return None


class ChordSelector(Frame):
    """controler which selector"""

    def __init__(self, noteselector, views):
        super().__init__()
        assert isinstance(views, list)
        self.noteselector = noteselector
        self.views = views
    def create_UI(self):


        def delete_listbox_values(listbox):
            ind = listbox.curselection()
            if not ind:return
            linename, key = listbox.get(ind[0])
            key.unset_values()
            listbox.delete(ind[0])


        registered_keys = ListboxValues(self)
        registered_keys.grid(row=1, column=1)
        registered_keys.bind("<BackSpace>", lambda event,l=registered_keys:delete_listbox_values(l))

        displayed_keys = ListboxValues(self)
        displayed_keys.grid(row=1, column=4)
        displayed_keys.bind("<BackSpace>", lambda event,l=displayed_keys:delete_listbox_values(l))

        def display():
            ind = registered_keys.curselection()
            if not ind: return
            linename, key = registered_keys.get(ind[0])
            if(ind):
                displayed_keys.insert(0, key)
                registered_keys.delete(ind[0])
                key.generate()

        Button(self, text="->", command=display).grid(row=1, column=3)

        def undisplay():
            ind = displayed_keys.curselection()
            if not ind: return
            linename, key = displayed_keys.get(ind[0])
            if(ind):
                registered_keys.insert(0, key)
                displayed_keys.delete(ind[0])
                key.unset_values()

        Button(self, text="<-", command=undisplay).grid(row=1, column=2)

        def AddNote():
            sig = self.noteselector.getCurSignal()
            if not sig: return
            for v in self.views:
                sig.attach(v)
            registered_keys.insert(0, sig)
        Button(self, text="AddNote", command=AddNote).grid(row=0, column=1)
