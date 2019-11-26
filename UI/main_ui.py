import sys
import subprocess
import webbrowser

from tkinter import Tk,Button,Label,Menu,Toplevel,messagebox
from tkinter.ttk import Notebook,Frame,LabelFrame
from tkinter import filedialog

from UI.piano_mvc import *
from UI.IHM_visualizer import *
import Utils.wav_create_notes_from_frequencies_db

class MainUI (Tk):
    """This is the main UI class. It is responsible for the module linking."""

    def on_closing(self):
        if messagebox.askokcancel("Avertissement fermeture", "Voulez-vous vraiment quitter l'application?"):
            self.destroy()

    def __init__(self):
        Tk.__init__(self)

        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()

        self.resizable(False, False)
        self.geometry("1000x620+"+str(int(w/2.0-750))+"+"+str(int(h/2.0-310)))
        self.title("La leçon de piano - Beta Version - Do not distribute")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        ######################################################################
        #                           Menubar init
        ######################################################################

        menu_bar = Menu()
        self.config(menu = menu_bar)

        subframe_menu = Notebook(self)
        subframe_menu.pack(fill="both", expand="yes")

        ######################################################################
        #                         Fenêtre Affichage
        ######################################################################

        def on_plotter_frame_closing():
            self.plotter_frame.withdraw()

        self.plotter_frame = Toplevel(self)
        self.plotter_frame.geometry("500x310+"+str(int(w/2.0+250))+"+"+str(int(h/2.0-310)))
        self.plotter_frame.title("Affichage des notes");
        self.plotter_frame.protocol("WM_DELETE_WINDOW", on_plotter_frame_closing)
        self.plotter=View(self.plotter_frame)
        self.plotter.grid(4)
        self.plotter.packing()
        #label3 = Label(self.plotter_frame, text="Affichage ici").pack()

        ######################################################################
        #                         Mode Generation
        ######################################################################

        frame0 = Frame(subframe_menu)
        frame0.pack()
        subframe_menu.add(frame0, text="Génération")

        IHM = NoteSelector(frame0)
        IHM.create_UI()
        IHM.pack(fill="both", side="top", expand="yes")

        ######### Left: notes
        #frame1 = Frame(frame0, padx=20, pady=20);
        #frame1.pack(fill="both", side="left", expand="yes")
        #label1 = Label(frame1, text="Générer note ici").pack()

        ss = SignalsSelector(IHM, [self.plotter], master=frame0, text="SignalSelector", padx=20, pady=20)
        ss.create_UI()
        ss.pack(fill="both", side="left", expand="yes")

        ######### Right: accords
        #frame2 = LabelFrame(frame0, text="Génération des accords", padx=20, pady=20);
        #frame2.pack(fill="both", side="right", expand="yes")
        #label2 = Label(frame2, text="Générer accords ici").pack()
        speaker = Speaker()
        chordsel = ChordSelector(IHM, [speaker], master=frame0,text="ChordSelector", padx=20, pady=20)
        chordsel.create_UI()
        chordsel.pack(fill="both", side="right", expand="yes")




        ######################################################################
        #                          Mode Clavier
        ######################################################################

        frame4 = LabelFrame(subframe_menu, text="Clavier", padx=20, pady=20);
        frame4.pack()
        subframe_menu.add(frame4, text="Clavier")

        octaves = 3
        piano = Piano(frame4, octaves, 45, 210)
        piano.packing()

        ######################################################################
        #                          Menubar linking
        ######################################################################

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Quitter", command=self.on_closing)
        menu_bar.add_cascade(label="Fichier", menu=file_menu)

        ###################
        edition_menu = Menu(menu_bar, tearoff=0)
        def regen_data():
            Utils.wav_create_notes_from_frequencies_db.generate()
        edition_menu.add_command(label="Recharger Tout", command=regen_data)
        def reset_data():
            folder = os.path.realpath(os.curdir)+"/Sounds"
            for f in os.listdir(folder):
                file_path = os.path.join(folder, f)
                try:
                    if file_path.endswith(".wav",) and os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            regen_data()
            ss.execute_on_elements(0, -1, callback=Signal.unset_values)
            ss.empty()
            chordsel.execute_on_elements(0, -1, callback=Signal.reset_wavname)
            chordsel.empty()
        edition_menu.add_command(label="Rétablir Défaut", command=reset_data)
        menu_bar.add_cascade(label="Edition", menu=edition_menu)

        #############
        window_menu = Menu(menu_bar, tearoff=0)
        window_submenu1 = Menu(window_menu, tearoff=0)
        ###################
        window_submenu1.add_command(label="Afficheur Onde", command=self.plotter_frame.deiconify)
        window_submenu1.add_command(label="Afficheur Harmonique", state="disabled")
        ###################
        window_menu.add_cascade(label="Ouvrir Vue", menu=window_submenu1)
        #############
        def open_all():
            self.plotter_frame.deiconify()
        window_menu.add_command(label="Ouvrir Tout", command=open_all)
        window_menu.add_separator()
        #############
        def reset_view():
            self.geometry("1000x620+"+str(int(w/2.0-750))+"+"+str(int(h/2.0-310)))
            self.plotter_frame.geometry("500x310+"+str(int(w/2.0+250))+"+"+str(int(h/2.0-310)))
        window_menu.add_command(label="Rétablir défaut", command=reset_view)
        ##################
        menu_bar.add_cascade(label="Fenêtre", menu=window_menu)
        help_menu = Menu(menu_bar, tearoff=0)

        def support_cb():
            webbrowser.open("https://github.com/WexyR/CAI_IHM/issues")
        help_menu.add_command(label="Support", command = support_cb)
        def credits_cb():
            webbrowser.open("https://github.com/WexyR/CAI_IHM/graphs/contributors")
        help_menu.add_command(label="Crédits", command=credits_cb)
        def help_cb():
            webbrowser.open("file://"+os.getcwd()+"/README.md")
        help_menu.add_command(label="Aide", command=help_cb)
        menu_bar.add_cascade(label="Aide", menu=help_menu)

    def toggleToplevel(level):
        self.plotter_frame.deiconify()

if __name__ == "__main__":
    app = MainUI()
    app.mainloop()
