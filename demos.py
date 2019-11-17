import sys
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
        from UI.frequencies_viewer import *
        root=Tk()
        root.title("Piano : Nom-Prenom")
        view=View(root)
        s1 = Signal("S1", 1, 1, 0, 0)
        s1.attach(view)
        s2 = Signal("S2", 1, 2, 0, 1)
        s2.attach(view)
        view.grid(4)
        view.packing()
        root.mainloop()
    elif(arg == '2'):
        from UI.IHM_visualizer import *
        mw = Tk()

        view=View(mw)
        IHM = NoteSelector(mw)
        IHM.create_UI()
        IHM.pack()
        ss = SignalsSelector(IHM, [view], text="SignalSelector")
        ss.create_UI()
        ss.pack()
        chordsel = ChordSelector(IHM, [], text="ChordSelector")
        chordsel.create_UI()
        chordsel.pack()
        view.grid(4)
        view.packing()
        mw.mainloop()
