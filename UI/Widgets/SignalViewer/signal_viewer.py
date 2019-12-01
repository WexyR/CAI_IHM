import sys, os
from math import sin,pi
from random import choice
from Utils.observer import *
from Utils.signal import *
from Utils.wav_audio import save_wav
from tkinter import Tk,Canvas, messagebox
from tkinter import filedialog

# TODO: remove unused imports

class SignalViewer(Observer):
    '''Mainly a View for an integrated list of Signal'''
    def __init__(self,parent,bg="white",width=600,height=300):
        self.canvas=Canvas(parent,bg=bg,width=width,height=height)
        self.signals={}
        self.width,self.height=width,height
        self.units=1
        self.canvas.bind("<Configure>",self.resize)

    def update(self, subject):
        print("View : update()")
        # print(args)
        if "id"+str(id(subject)) not in self.signals.keys():
            print("update not in keys")
            self.signals["id"+str(id(subject))] = subject
        else:
            print("update in keys -> delete curve")
            self.canvas.delete("id"+str(id(subject)))
        self.plot_signal(subject, "id"+str(id(subject)))

    def plot_signal(self,signal,name):
        if signal.color:
            color = signal.color
        else:
            color= "red"
        if (signal.values is None or len(signal.values)==0):
            print("values is None")
            self.canvas.delete(name)
            return
        w,h=self.width,self.height
        signal_id=None
        if signal.values and len(signal.values) > 1:
            plot = [(x*w,h/2.0*(1-y/(self.units/2.0))) for (x, y) in signal.values]
            signal_id=self.canvas.create_line(plot, fill=color, smooth=1, width=3,tags=name)
            
        return signal_id

    def grid(self,steps=2):
        self.units=steps
        tile_x=self.width/steps
        for t in range(1,steps+1):
            x =t*tile_x
            self.canvas.create_line(x,0,x,self.height,tags="grid")
            self.canvas.create_line(x,self.height/2-10,x,self.height/2+10,width=3,tags="grid")
        tile_y=self.height/steps
        for t in range(1,steps+1):
            y =t*tile_y
            self.canvas.create_line(0,y,self.width,y,tags="grid")
            self.canvas.create_line(self.width/2-10,y,self.width/2+10,y,width=3,tags="grid")

    def resize(self,event):
        if event:
            self.width,self.height=event.width,event.height
            self.canvas.delete("grid")
            for signal_name,signal_values in self.signals.items():
                self.canvas.delete(signal_name)
                self.plot_signal(signal_values, signal_name)
            self.grid(self.units)

    def packing(self) :
        self.canvas.pack(expand=1,fill="both",padx=6)

if  __name__ == "__main__" :
    root=Tk()
    root.title("Piano : Nom-Prenom")
    view=View(root)
    s1 = Signal("S1", 1, 1, 0, 0)
    s1.attach(view)
    s2 = Signal("S2", 1, 2, 0, 1)
    s2.attach(view)
    view.grid(4)
    view.packing()
    s1.generate()
    s2.generate()
    root.mainloop()
