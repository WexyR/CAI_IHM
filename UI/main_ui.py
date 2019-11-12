import sys
if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import Tk,Frame,Button,Label,LabelFrame,Menu,Notebook,TopLevel
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import Tk,Frame,Button,Label,LabelFrame,Menu,Toplevel,messagebox
    from tkinter.ttk import Notebook
    from tkinter import filedialog

class MainUI (Tk):
    """This is the main UI class. It is responsible for the module linking."""

    def on_closing(self):
        if messagebox.askokcancel("Avertissement fermeture", "Voulez-vous vraiment quitter l'application?"):
            self.destroy()

    def __init__(self):
        Tk.__init__(self)

        self.geometry("600x350")
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
        #                         Mode Generation
        ######################################################################

        frame0 = Frame(subframe_menu)
        frame0.pack()
        subframe_menu.add(frame0, text="Génération")

        frame1 = LabelFrame(frame0, text="Génération de la note", padx=20, pady=20);
        frame1.pack(fill="both", side="left", expand="yes")

        label1 = Label(frame1, text="Générer note ici").pack()

        ###########

        frame2 = LabelFrame(frame0, text="Génération des accords", padx=20, pady=20);
        frame2.pack(fill="both", side="right", expand="yes")

        label2 = Label(frame2, text="Générer accords ici").pack()


        ######################################################################
        #                          Mode Clavier
        ######################################################################

        frame4 = LabelFrame(subframe_menu, text="Clavier", padx=20, pady=20);
        frame4.pack()
        subframe_menu.add(frame4, text="Clavier")

        label4 = Label(frame4, text="Clavier ici").pack()

        ######################################################################
        #                         Fenêtre Affichage
        ######################################################################

        self.plotter_frame = Toplevel(self)
        self.plotter_frame.geometry("400x200")
        #self.plotter_frame.withdraw()
        self.plotter_frame.title("Affichage des notes");

        def on_plotter_frame_closing():
            self.plotter_frame.withdraw()

        self.plotter_frame.protocol("WM_DELETE_WINDOW", on_plotter_frame_closing)

        label3 = Label(self.plotter_frame, text="Affichage ici").pack()

        ######################################################################
        #                          Menubar linking
        ######################################################################

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Quitter")
        menu_bar.add_cascade(label="Fichier", menu=file_menu)

        edition_menu = Menu(menu_bar, tearoff=0)
        edition_menu.add_command(label="Regenérer Tout")
        edition_menu.add_command(label="Rétablir Défaut")
        menu_bar.add_cascade(label="Edition", menu=edition_menu)

        window_menu = Menu(menu_bar, tearoff=0)
        window_submenu1 = Menu(window_menu, tearoff=0)
        window_submenu1.add_command(label="Afficheur Onde", command=self.plotter_frame.deiconify)
        window_submenu1.add_command(label="Afficheur Harmonique")
        window_menu.add_cascade(label="Ouvrir Vue", menu=window_submenu1)
        window_menu.add_command(label="Ouvrir Tout")
        window_menu.add_separator()
        window_menu.add_command(label="Rétablir défaut")
        menu_bar.add_cascade(label="Fenêtre", menu=window_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Support")
        help_menu.add_command(label="Crédits")
        menu_bar.add_cascade(label="Aide", menu=help_menu)

    def toggleToplevel(level):
        self.plotter_frame.deiconify()
