import sys
import collections
import subprocess
import os

from tkinter import Tk,Frame,Button,Label
from tkinter import filedialog
from observer import *

class Piano :
    '''piano widget'''
    def __init__(self,parent,octaves, key_w=50, key_h=220) :
        self.parent=parent
        self.octaves=[]
        self.frame=Frame(self.parent,bg="yellow")
        for octave in range(octaves) :
            self.create_octave(self.frame,octave+2, key_w=key_w, key_h=key_h)
    def create_octave(self,parent,degree=3, key_w=50, key_h=220) :
        frame=Frame(parent,bg="green")
        model=Octave(degree)
        self.octaves.append(model)
        control=Keyboard(frame,model, key_w=key_w, key_h=key_h)
        view=Screen(frame)
        model.attach(view)
        view.get_screen().pack()
        control.get_keyboard().pack()
        frame.pack(side="left",fill="x",expand=True)
    def packing(self) :
        self.frame.pack(fill="both", side="right", expand="yes")

if __name__ == "__main__" :
    root = Tk()
    octaves=3
    root.geometry(str(280*octaves)+"x300")
    root.title("La leçon de piano à "+ str(octaves) + " octaves")
    piano=Piano(root,octaves)
    piano.packing()
    root.mainloop()
