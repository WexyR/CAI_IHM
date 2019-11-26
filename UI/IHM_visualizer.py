from UI.frequencies_viewer import View, Signal
from observer import Subject, Observer
from Generation.frequencies_db_init import *
from Utils.wav_audio import *

import subprocess

import sys
import os
import re

if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import Tk, Frame, LabelFrame, StringVar, IntVar, DoubleVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox, Radiobutton, Scale, Entry, messagebox
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import Tk, Frame, LabelFrame, StringVar, IntVar, DoubleVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox, Radiobutton, Scale, Entry, messagebox
    from tkinter import filedialog

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

class WAVmodel(Subject):
    """model, represent the list of all wav signal"""

    def __init__(self):
        super().__init__()
        self.note_wavs = {}
        self.chord_wav = {}

    def update_data(self, paths=["Sounds/"]):
        l_dir = []
        for path in paths:
            l_dir += [(path,file_name) for file_name in os.listdir(path) if os.isfile(file_name)]


        for key in self.note_wavs.keys():
            if(key[1].split("_")[0] == ""): #doesn't need
                continue
            if(key not in l_dir): # file deleted
                del self.note_wavs[key]

        keys = self.note_wavs.keys()
        for key in l_dir:
            if(key not in keys):
                path, file_name = key


    def register_signal(self, signal):
        keyname = signal.get_wavname_by_data()
        if(keyname in self.note_wavs.keys()):
            messagebox.showwarning("Already existing signal", "This signal is already existing. Aborting creation.")
            return -1




    def get(self, regular_expression=None):
        """return all wavs which have a match with the regular_expression in the name"""
        if regular_expression is None:
            return self.wavs
        else:
            pass
            # return set([elem for elem in self.wavs if re.match(regular_expression,elem.wavname)])


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


class NoteRegisterer(LabelFrame):
    """controler which selector"""

    def __init__(self, noteselector, views, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        assert isinstance(views, list)
        self.noteselector = noteselector
        self.views = views
        self.left_listbox = None
        self.right_listbox = None
        self.button_toleft = None
        self.button_toright = None
        self.add_button = None
        self.left_listbox_label = None
        self.right_listbox_label = None

    def create_UI(self):

        self.left_listbox_label = Label(self, text="left_listbox")
        self.left_listbox_label.grid(row=1, column=1)
        self.left_listbox = ListboxValues(self, height=5)
        self.left_listbox.grid(row=2, column=1)
        self.left_listbox.bind("<BackSpace>", lambda event,l=self.left_listbox:self.delete_listbox_values(l,Signal.unset_values))

        self.right_listbox_label = Label(self, text="right_listbox")
        self.right_listbox_label.grid(row=1, column=4)
        self.right_listbox = ListboxValues(self, height=5)
        self.right_listbox.grid(row=2, column=4)
        self.right_listbox.bind("<BackSpace>", lambda event,l=self.right_listbox:self.delete_listbox_values(l,Signal.unset_values))



        self.button_toright=Button(self, text="->",command=lambda:self.move_listbox_value(self.left_listbox, self.right_listbox))#, command=lambda:self.move_listbox_value(self.left_listbox, self.right_listbox, Signal.generate)).grid(row=1, column=3)
        self.button_toright.grid(row=2, column=3)
        self.button_toleft=Button(self, text="<-",command=lambda:self.move_listbox_value(self.right_listbox, self.left_listbox))#, command=lambda:self.move_listbox_value(self.right_listbox, self.left_listbox, Signal.unset_values)).grid(row=1, column=2)
        self.button_toleft.grid(row=2, column=2)


        self.add_button = Button(self, text="AddNote", command=self.add_note)
        self.add_button.grid(row=0, column=1)

    def delete_listbox_values(self, listbox, callback=None, *cbargs, **cbkwargs):
        ind = listbox.curselection()
        if not ind:return
        linename, key = listbox.get(ind[0])
        if(callback):
            callback(key, *cbargs, **cbkwargs)
        listbox.delete(ind[0])

    def move_listbox_value(self, from_listbox, to_listbox, callback=None, *cbargs, **cbkwargs):
        ind = from_listbox.curselection()
        if not ind: return
        linename, key = from_listbox.get(ind[0])
        to_listbox.insert(0, key)
        from_listbox.delete(ind[0])
        if(callback):
            callback(key, *cbargs, **cbkwargs)

    def add_note(self, listbox=None, validatecallback=None, *cbargs, **cbkwargs):
        if listbox is None: listbox=self.left_listbox;
        sig = self.noteselector.getCurSignal()
        if not sig: return -1
        if validatecallback is not None:
            if not validatecallback(sig, *cbargs, **cbkwargs):
                return -2

        for v in self.views:
            sig.attach(v)
        listbox.insert(0, sig)
    def empty(self, side="both"):
        assert isinstance(side, str)
        side = side.lower()
        assert side in ("left", "right", "both")

        if side in ("left", "both"):
            self.left_listbox.delete(0, self.left_listbox.size()-1)
        if side in ("right", "both"):
            self.right_listbox.delete(0, self.right_listbox.size()-1)

    def execute_on_elements(self, start, end=None, side="both", callback=None, *args, **kwargs):
        """execute a callback function on some elements of the listboxes
        start: start index of elements
        end: end index of elements
          --- None : only the element at start will be concerned
          --- -1   : all elements will be concerned
        side: listbox concerned
          --- "both"
          --- "left"
          --- "right"
        callback: function to execute on elements with every other parameters given
                  callback(element, *cbargs, **cbkwargs)"""
        assert isinstance(side, str)
        side = side.lower()
        assert side in ("left", "right", "both")

        if side in ("left", "both"):
            if callback is not None:

                if end is None:
                    callback(self.left_listbox.get(start)[1], *args, **kwargs)
                else:
                    if end == -1:
                        end = self.left_listbox.size()-1
                    elements = self.left_listbox.get(start, end)
                    print(elements)
                    for _, element in elements:
                        callback(element, *args, **kwargs)
        if side in ("right", "both"):
            if callback is not None:
                if end is None:
                    callback(self.right_listbox.get(start)[1], *args, **kwargs)
                else:
                    if end == -1:
                        end = self.right_listbox.size()-1
                    elements = self.right_listbox.get(start, end)
                    for _, element in elements:
                        callback(element, *args, **kwargs)

class SignalsSelector(NoteRegisterer):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

    def create_UI(self):
        super().create_UI()
        self.left_listbox_label.configure(text="signals")
        self.right_listbox_label.configure(text="displayed signals")

        self.button_toright.configure(command=lambda:self.move_listbox_value(self.left_listbox, self.right_listbox, Signal.generate))
        self.button_toleft.configure(command=lambda:self.move_listbox_value(self.right_listbox, self.left_listbox, Signal.unset_values))

class ChordSelector(NoteRegisterer):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

    def generate_signal_wav(self, sig, force_generation):
        generation_status = sig.generate_sound(force=force_generation)
        if(generation_status == 0): #if succesfully generated
            messagebox.showinfo("wav generated", "{0} file has succesfully been generated".format(sig.wavname))
        elif generation_status == -1:
            messagebox.showerror("Generation Error", "Error while generating wav file. Aborting...")

            return -1
        elif generation_status == 1:
            is_yes = messagebox.askyesno("Already existing file","Already existing file, do you want to overwrite it ?")
            if is_yes:
                return self.generate_signal_wav(sig, True)

    def play_signal_sound(self, sig):
        if(sig.play() == -1):
            messagebox.showwarning("Play", "No file has been found for this note")

    def create_UI(self):

        ### super() modifications
        super().create_UI()
        self.left_listbox_label.configure(text="notes")
        self.right_listbox_label.configure(text="chord")
        self.right_listbox.configure(height=3)

        def select_chord_cb():

            if self.right_listbox.size() < 3:
                self.move_listbox_value(self.left_listbox, self.right_listbox, Signal.generate)

        self.button_toright.configure(command=select_chord_cb)
        self.button_toleft.configure(command=lambda:self.move_listbox_value(self.right_listbox, self.left_listbox, Signal.unset_values))

        def validatecallback(sig):
            if sig.keyname is None or sig.keyname == "":
                messagebox.showerror("Error", "Only note (not frequency) signal can be selected")
                return False
            else:
                return True


        def generate_and_add():
            sig = self.noteselector.getCurSignal()
            generation = self.generate_signal_wav(sig, False)
            if(generation == -1):
                messagebox.showwarning("Generation","This sound has not been generated. Listening to this sound will be impossible. Try to generate it again")
            self.add_note(validatecallback=validatecallback)



        self.add_button.configure(command=generate_and_add)

        ### self additions

        def play_cursig():
            ind = self.left_listbox.curselection()
            if not ind:
                messagebox.showerror("Error", "No note selected")
                return
            linename, sig = self.left_listbox.get(ind[0])
            if(sig):
                self.play_signal_sound(sig)
            else:
                messagebox.showerror("Error", "No signal found")


        self.play_button = Button(self, text="Play sound", command=play_cursig)
        self.play_button.grid(row=4, column=1)

        def play_chord():
            wav_chord(file='chord.wav',frequencies=[i.split('_')[1] for i in self.right_listbox.get(0, -1)],framerate=8000,duration=2)
            subprocess.call(["aplay", "Sounds/chord.wav"])
        self.playchord_button = Button(self, text="Play chord", command=play_chord)
        self.playchord_button.grid(row=4, column=4)


class Speaker(Observer):
    def __init__(self):
        super().__init__()

    def update(self, sig):
        if(sig.isplaying):
            if(os.path.exists("Sounds/"+sig.wavname)):
                subprocess.call(["aplay", "Sounds/"+sig.wavname])
