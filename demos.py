import sys
from tkinter import *

from UI.Widgets.Piano.piano_model import *
from UI.Widgets.Piano.piano_view import *
from UI.Widgets.Piano.piano_controller import *

from UI.Widgets.SignalViewer.signal_viewer import *

from UI.Widgets.SignalGenerator.note_selector import *
from UI.Widgets.SignalGenerator.note_registerer import *
from UI.Widgets.SignalGenerator.signals_registerer import *

from Utils.speaker import *
from Utils.signals_model import *

if __name__ == "__main__":
    if sys.version_info.major != 3:
        print("This program must be executed using python 3.X You are currently using python " \
        +str(sys.version_info.major)+"."+str(sys.version_info.minor))
        sys.exit(0)
    if len(sys.argv) <= 1:
        print("Missing parameter {1 2}. See README.md for more information.")
        sys.exit(0)
    arg = sys.argv[1]
    print("Selected program: "+arg)
    if(arg == '1'):
        root=Tk()
        root.title("Piano : Nom-Prenom")
        view=SignalViewer(root)
        s1 = Signal("S1", 1, 1, 0, 0)
        s1.attach(view)
        s2 = Signal("S2", 1, 2, 0, 1)
        s2.attach(view)
        view.grid(4)
        view.packing()
        root.mainloop()
    elif(arg == '2'):
        mw = Tk()

        view=SignalViewer(mw)
        speaker = Speaker()
        IHM = NoteSelector(mw)
        IHM.create_UI()
        IHM.pack()
        model = SignalsModel([view, speaker])
        sr = SignalsRegisterer(mw, IHM, model, [view], text="signal")
        sr.create_UI()
        sr.pack()
        nr = NoteRegisterer(mw, IHM, model, [speaker], text="note")
        nr.create_UI()
        nr.pack()
        # chordsel = ChordSelector(IHM, [], text="ChordSelector")
        # chordsel.create_UI()
        # chordsel.pack()

        model.update_note_data(["Sounds/"])
        view.grid(4)
        view.packing()
        mw.mainloop()
