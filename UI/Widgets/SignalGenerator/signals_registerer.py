import subprocess
import sys
import os
import re

from UI.Widgets.SignalListbox.listbox_values import *

from Utils.observer import Subject, Observer
from Utils.wav_audio import *
from Utils.signal import *

from Generation.frequencies_db_init import *

from tkinter import Tk, Frame, LabelFrame, StringVar, IntVar, DoubleVar, OptionMenu, Checkbutton, Spinbox, Label, Button, Listbox, Radiobutton, Scale, Entry, messagebox
from tkinter import filedialog

# TODO: Remove unnecessary import

class SignalsRegisterer(LabelFrame):
    """controler which selector"""

    def __init__(self, master, noteselector, model, views, *arg, **kwarg):
        super().__init__(master, *arg, **kwarg)
        if not isinstance(views, list):
            print("/!\\warning/!\\, depreciation: views arguments is not a list. Automatically converted to list")
            views = list(views)
        self.noteselector = noteselector
        self.model = model
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



        self.button_toright=Button(self, text="->")#,command=lambda:self.move_listbox_value(self.left_listbox, self.right_listbox))#, command=lambda:self.move_listbox_value(self.left_listbox, self.right_listbox, Signal.generate)).grid(row=1, column=3)
        self.button_toright.grid(row=2, column=3)
        self.button_toleft=Button(self, text="<-")#,command=lambda:self.move_listbox_value(self.right_listbox, self.left_listbox))#, command=lambda:self.move_listbox_value(self.right_listbox, self.left_listbox, Signal.unset_values)).grid(row=1, column=2)
        self.button_toleft.grid(row=2, column=2)


        self.add_button = Button(self, text="Générer Signal", command=self.add_note)
        self.add_button.grid(row=0, column=1)

        self.left_listbox_label.configure(text="signals")
        self.right_listbox_label.configure(text="displayed signals")

        self.button_toright.configure(command=lambda:self.move_listbox_value(self.left_listbox, self.right_listbox, Signal.generate))
        self.button_toleft.configure(command=lambda:self.move_listbox_value(self.right_listbox, self.left_listbox, Signal.unset_values))

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

    # def empty(self, side="both"):
    #     assert isinstance(side, str)
    #     side = side.lower()
    #     assert side in ("left", "right", "both")
    #
    #     if side in ("left", "both"):
    #         self.left_listbox.delete(0, self.left_listbox.size()-1)
    #     if side in ("right", "both"):
    #         self.right_listbox.delete(0, self.right_listbox.size()-1)

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
