import subprocess
import sys
import os
import re

from Utils.observer import Subject, Observer
from Utils.wav_audio import *
from Utils.chord import *

from UI.Widgets.SignalListbox.listbox_values_observer import *

from Generation.frequencies_db_init import *

from tkinter import Tk, Frame, LabelFrame, StringVar, IntVar, DoubleVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox, Radiobutton, Scale, Entry, messagebox
from tkinter import filedialog

# TODO: Remove unnecessary import

class NoteRegisterer(LabelFrame):
    def __init__(self, master, noteselector, model, views, *arg, model_path=["Sounds/", "Sounds/Chords/"], **kwarg):
        super().__init__(master, *arg, **kwarg)
        if not isinstance(views, list):
            print("/!\\warning/!\\, depreciation: views arguments is not a list. Automatically converted to list")
            views = list(views)
        self.noteselector = noteselector

        self.left_listbox = ListboxValuesObs(self, dirpath=["Sounds/"], height=5)
        model.attach(self.left_listbox)

        self.right_listbox = ListboxValuesObs(self, dirpath=["Sounds/Chords"], height=5)
        model.attach(self.right_listbox)

        self.views = views

        self.model = model
        self.model_path = model_path

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
        self.left_listbox.configure(selectmode='multiple')
        self.left_listbox.bind("<BackSpace>", lambda event,l=self.left_listbox:self.delete_listbox_values(l,Signal.reset_wavname))

        self.right_listbox_label = Label(self, text="chords")
        self.right_listbox_label.grid(row=1, column=3)
        self.right_listbox.grid(row=2, column=3)
        self.right_listbox.bind("<BackSpace>", lambda event,l=self.right_listbox:self.delete_listbox_values(l,Signal.reset_wavname))

        def generate_and_add():
            sig = self.noteselector.getCurSignal()
            generation = self.generate_signal_wav(sig, False)
            if(generation == -1):
                messagebox.showwarning("Generation","This sound has not been generated. Listening to this sound will be impossible. Try to delete it then generate it again")
            self.model.update_note_data(self.model_path)

        self.add_button = Button(self, text="Générer Son", command=generate_and_add)
        self.add_button.grid(row=0, column=1)

        def fuse_and_add():
            signals = [self.left_listbox.get(i)[1] for i in self.left_listbox.curselection()]
            if(len(signals) <= 1):
                messagebox.showwarning("Generation","La génération d'un accord requiere 2 ou plus notes. Vous pouvez en sélectionner dans la liste 'notes'.")
            chord = Chord(signals=signals)
            chord.generate_sound()
            self.model.update_data()

        self.add_chord_button = Button(self, text="Générer Accord", command=fuse_and_add)
        self.add_chord_button.grid(row=0, column=3)

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
            chord = self.right_listbox.curselection()[1]
            if(chord.play() == -1):
                messagebox.showwarning("Play", "No file has been found for this chord")
            #subprocess.call(["aplay", self.chords_model_path+chord.__str__()])
        self.playchord_button = Button(self, text="Play chord", command=play_chord)
        self.playchord_button.grid(row=4, column=3)
