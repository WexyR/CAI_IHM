from math import sin,pi
from random import choice
from observer import *
from Utils.wav_audio import save_wav
## from pylab import linspace,sin

import sys, os
if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import Tk,Canvas, messagebox
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import Tk,Canvas, messagebox
    from tkinter import filedialog


class Signal(Subject):
    """Signal class"""
    def __init__(self, magnitude=1.0, frequency=1.0, phase=0.0, N_harm=0, duration=2, keyname="", color=None):
        Subject.__init__(self)
        self.set(magnitude, frequency, phase, N_harm, duration, keyname, color)

        self.values = None
        self.wavname = None
        self.isplaying = False

    def __str__(self):
        if self.wavname is None:
            return self.keyname + " f:" + str(int(self.frequency)) + " N:" + str(self.N_harm)
        else:
            return self.wavname

    def set(self, magnitude=1.0, frequency=1.0, phase=0.0, N_harm=0, duration=2, keyname="", color=None):
        self.magnitude = magnitude
        self.frequency = frequency
        self.phase = phase
        self.N_harm = N_harm
        self.duration = duration
        self.keyname = keyname

        if color is None:
            self.color = "#" + "".join([choice("0123456789ABCDEF") for _ in range(6)])
        else:
            self.color = color

    def harmonize(self, t, N=0):
        a,f,p=self.magnitude,self.frequency,self.phase
        return sum([(a/h)*sin(2*pi*(f*h)*t-p) for h in range(1, N+2)])

    def generate(self, period=2, samples=100):
        Tech = period/samples
        print("Tech",Tech,period,samples)
        self.values = [(t*Tech,self.harmonize(t*Tech, self.N_harm)) for t in range(int(samples)+1)]
        self.notify()
        return self.values

    def unset_values(self):
        if(self.values is not None):
            self.values.clear()
            self.notify()

    def generate_sound(self, force=False):
        wavname = self.get_wavname_by_data()

        existing_file = os.path.exists("Sounds/"+wavname)

        print(existing_file)

        if(not force and existing_file):
            self.wavname = wavname
            return 1 #already generated file

        try:
            framerate = 8000
            wav_values = [30000 * self.harmonize(t/framerate, self.N_harm) for t in range(int(framerate*self.duration))]
            save_wav(wavname, wav_values, framerate)


            success = True
        except Exception as e:
            print(e)
            success = False

        if(success):
            self.wavname = wavname
            return 0 #sucess
        else:
            return -1 #error

    def play(self):
        if self.wavname is not None:
            self.isplaying = True
            self.notify()
            self.isplaying = False
            return 0
        else:
            return -1


    def get_wavname_by_data(self):
        return "{0}_{1:.2f}_{2}_{3}s.wav".format(self.keyname, self.frequency, self.N_harm, self.duration)


class View(Observer):
    def __init__(self,parent,bg="white",width=600,height=300):
        self.canvas=Canvas(parent,bg=bg,width=width,height=height)
        self.signals={}
        self.width,self.height=width,height
        self.units=1
        self.canvas.bind("<Configure>",self.resize)



    def update(self, subject=None):
        print("View : update()")
        print(subject)
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
        print(name)
        if (signal.values is None or len(signal.values)==0):
            print("values is None")
            self.canvas.delete(name)
            return
        w,h=self.width,self.height
        signal_id=None
        if signal.values and len(signal.values) > 1:
            print(self.units)
            plot = [(x*w,h/2.0*(1-y/(self.units/2.0))) for (x, y) in signal.values]
            signal_id=self.canvas.create_line(plot, fill=color, smooth=1, width=3,tags=name)
            print(signal_id)
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
