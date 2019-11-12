from math import sin,pi
from observer import *
## from pylab import linspace,sin

import sys
if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import Tk,Canvas
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import Tk,Canvas
    from tkinter import filedialog


class Signal(Subject):
    """Signal class"""
    def __init__(self, name, magnitude=1.0, frequency=1.0, phase=0.0, N_harm=0):
        Subject.__init__(self)
        self.name = name

        self.magnitude = magnitude
        self.frequency = frequency
        self.phase = phase
        self.N_harm = N_harm

        self.values = None

    def harmonize(self, t, N=0):
        a,f,p=self.magnitude,self.frequency,self.phase
        return sum([(a/h)*sin(2*pi*(f*h)*t-p) for h in range(1, N+2)])

    def generate(self, period=2, samples=100):
        Tech = period/samples
        print("Tech",Tech,period,samples)
        self.values = [(t*Tech,self.harmonize(t*Tech, self.N_harm)) for t in range(int(samples)+1)]
        print(self.values)
        self.notify()
        return self.values

class View(Observer):
    def __init__(self,parent,bg="white",width=600,height=300):
        self.canvas=Canvas(parent,bg=bg,width=width,height=height)
        self.signals={}
        self.width,self.height=width,height
        self.units=1
        self.canvas.bind("<Configure>",self.resize)



    def update(self, subject=None):
        print("View : update()")
        if subject.name not in self.signals.keys():
            self.signals[subject.name] = subject.values
        else:
            self.canvas.delete(subject.name)
        self.plot_signal(subject.values, subject.name)

    def plot_signal(self,signal,name,color="red"):
        w,h=self.width,self.height
        signal_id=None
        if signal and len(signal) > 1:
            print(self.units)
            plot = [(x*w,h/2.0*(1-y/(self.units/2.0))) for (x, y) in signal]
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
