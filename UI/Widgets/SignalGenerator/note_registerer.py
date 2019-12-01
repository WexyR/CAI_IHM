import subprocess
import sys
import os
import re

from Utils.observer import Subject, Observer
from Utils.wav_audio import *

from UI.Widgets.SignalListbox.listbox_values_observer import *

from Generation.frequencies_db_init import *

from tkinter import Tk, Frame, LabelFrame, StringVar, IntVar, DoubleVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox, Radiobutton, Scale, Entry, messagebox
from tkinter import filedialog

# TODO: Remove unnecessary import
class NoteRegisterer(LabelFrame):
    def __init__(self, master, noteselector, model, views, *arg, **kwarg):
        super().__init__(master, *arg, **kwarg)
        if not isinstance(views, list):
            print("/!\\warning/!\\, depreciation: views arguments is not a list. Automatically converted to list")
            views = list(views)
        self.noteselector = noteselector
        self.left_listbox = ListboxValuesObs(self, height=5)
        model.attach(self.left_listbox)
        self.views = views
        self.model = model

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

    def delete_listbox_values(self, listbox, callback=None, *cbargs, **cbkwargs):
        ind = listbox.curselection()
        if not ind:return
        linename, key = listbox.get(ind[0])
        if(callback):
            callback(key, *cbargs, **cbkwargs)
        listbox.delete(ind[0])

    def play_signal_sound(self, sig):
        if(sig.play() == -1):
            messagebox.showwarning("Play", "No file has been found for this note")

    def create_UI(self):

        ### super() modifications
        self.left_listbox_label = Label(self, text="notes")
        self.left_listbox_label.grid(row=1, column=1)
        self.left_listbox.grid(row=2, column=1)
        self.left_listbox.bind("<BackSpace>", lambda event,l=self.left_listbox:self.delete_listbox_values(l,Signal.reset_wavname))


        # self.left_listbox_label.configure(text="notes")
        # self.right_listbox_label.configure(text="chord")
        # self.right_listbox.configure(height=3)

        # def select_chord_cb():
        #
        #     if self.right_listbox.size() < 3:
        #         self.move_listbox_value(self.left_listbox, self.right_listbox, Signal.generate)

        # self.button_toright.configure(command=select_chord_cb)
        # self.button_toleft.configure(command=lambda:self.move_listbox_value(self.right_listbox, self.left_listbox, Signal.unset_values))



        def generate_and_add():
            sig = self.noteselector.getCurSignal()
            generation = self.generate_signal_wav(sig, False)
            if(generation == -1):
                messagebox.showwarning("Generation","This sound has not been generated. Listening to this sound will be impossible. Try to delete it then generate it again")
            self.model.update_note_data()

            self.add_button = Button(self, text="AddNote", command=generate_and_add)
            self.add_button.grid(row=0, column=1)



        # def add_note(self, listbox=None, validatecallback=None, *cbargs, **cbkwargs):
        #     if listbox is None: listbox=self.left_listbox;
        #     sig = self.noteselector.getCurSignal()
        #     if not sig: return -1
        #     if validatecallback is not None:
        #         if not validatecallback(sig, *cbargs, **cbkwargs):
        #             return -2
        #
        #     for v in self.views:
        #         sig.attach(v)
        #     listbox.insert(0, sig)

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
