from UI.frequencies_viewer import View, Signal
from observer import Subject, Observer

import sys
if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import Tk,Frame, StringVar, OptionMenu, Checkbutton, Spinbox, Label, Button
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import Tk,Frame,StringVar, OptionMenu, Checkbutton, Spinbox, Label, Button
    from tkinter import filedialog


class NoteSelector(Frame):
    """Note selection widget controller"""

    def __init__(self, parent, model=None, *arg, **kwarg):
        super().__init__(parent, *arg, **kwarg)
        self.model = model



    def _validate_spinbox(self, S, P):
        """[private] validation function of Spinbox widget"""
        if S == '' or P == '': return True
        result = False
        if (S.isdigit()):
            if(int(P)>=2 and int(P)<=5):
                result = True
        return result




    def create_UI(self):

        def sharpable(key, checkbox):
            if(key in "BE"):
                checkbox.deselect()
                checkbox.configure(state="disabled")
            else:
                checkbox.configure(state="normal")





        keys = tuple("ABCDEFG")
        keyvar = StringVar()
        keyvar.set(keys[0])
        sharpvar = StringVar()
        is_sharp = Checkbutton(self,text="#", variable=sharpvar, onvalue='#', offvalue='')
        om = OptionMenu(self, keyvar, *keys, command=lambda value=keyvar.get(), checkbox=is_sharp:sharpable(value, checkbox))
        om.grid(row=2, column=1)
        is_sharp.grid(row=2, column=2)

        Label(self, text="Octave 2-5").grid(row=1, column=3)

        vcmd_spinbox = (self.register(self._validate_spinbox), '%S', '%P')
        octave = Spinbox(self, from_=2, to=5, validate="all",validatecommand=vcmd_spinbox)
        octave.grid(row=2, column=3)

        Button(self, text="test", command=lambda k=keyvar, s=sharpvar:print(k.get() + s.get() + octave.get())).grid(row=2, column=4)







if __name__ == "__main__":
    mw = Tk()
    IHM = NoteSelector(mw)
    IHM.create_UI()
    IHM.pack()
    mw.mainloop()
