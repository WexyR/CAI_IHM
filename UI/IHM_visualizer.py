from UI.frequencies_viewer import View, Signal
from observer import Subject, Observer

import sys
if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import Tk,Frame, StringVar, OptionMenu, Checkbutton, Spinbox
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import Tk,Frame,StringVar, OptionMenu, Checkbutton, Spinbox
    from tkinter import filedialog


class NoteSelector(Frame):
    """Note selection widget controller"""

    def __init__(self, parent, model=None, *arg, **kwarg):
        super().__init__(parent, *arg, **kwarg)
        self.model = model


        # vcmd= (self.register(self._validate_spinbox), '%W', '%P')



    def create_UI(self):
        def sharpable(key, checkbox):
            if(key in "BE"):
                checkbox.deselect()
                checkbox.configure(state="disabled")
            else:
                checkbox.configure(state="normal")



        keys = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
        v = StringVar()
        v.set(keys[0])
        is_sharp = Checkbutton(self,text="#")
        om = OptionMenu(self, v, *keys, command=lambda value=v.get(), checkbox=is_sharp:sharpable(value, checkbox))
        om.pack(side="left")
        is_sharp.pack(side="left")

        octave = Spinbox(self, from_=2, to=5)
        octave.pack(side="left")








if __name__ == "__main__":
    mw = Tk()
    IHM = NoteSelector(mw)
    IHM.create_UI()
    IHM.pack()
    mw.mainloop()
