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

        ######################################################################
        #                         Fenêtre Affichage
        ######################################################################

        def on_plotter_frame_closing():
            plotter_frame.withdraw()

        plotter_frame = Toplevel()
        plotter_frame.geometry("500x310")
        plotter_frame.title("Affichage des notes");
        plotter_frame.protocol("WM_DELETE_WINDOW", on_plotter_frame_closing)
        plotter=SignalViewer(plotter_frame)
        plotter.grid(4)
        plotter.packing()

        ######################################################################
        #                         Speaker
        ######################################################################

        speaker = Speaker()

        ######################################################################
        #                         Mode Generation
        ######################################################################

        frame0 = Frame(mw)
        frame0.pack()
        #mw.add(frame0, text="Génération")

        IHM = NoteSelector(frame0)
        IHM.create_UI()
        IHM.pack(fill="both", side="top", expand="yes")

        frame1 = Frame(frame0)
        frame1.pack(fill="both", side="bottom", expand="yes")

        model = SignalsModel(inner_views=[plotter, speaker], paths=["Sounds/", "Sounds/Chords/"])
        sr = SignalsRegisterer(frame1, IHM, model, [plotter], text="Signaux")
        sr.create_UI()
        sr.pack(fill="both", side="left", expand="yes")


        chords_model = SignalsModel(inner_views=[plotter, speaker])
        nr = NoteRegisterer(frame1, IHM, model, [speaker], text="Notes")
        nr.create_UI()
        nr.pack(fill="both", side="right", expand="yes")

        model.update_data()
        mw.mainloop()
