import sys
if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import Tk,Frame,Button,Label,LabelFrame,Menu,Notebook
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import Tk,Frame,Button,Label,LabelFrame,Menu
    from tkinter.ttk import Notebook
    from tkinter import filedialog

class UI_Main:
    def __init__(self):
        root = Tk()
        root.geometry("600x350")
        root.title("La leçon de piano - Beta Version - Do not distribute")

        ######################################################################
        #                           Menus
        ######################################################################

        menu_bar = Menu()
        root.config(menu = menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edition_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=file_menu)

        window_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Window", menu=window_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        subframe_menu = Notebook(root)
        subframe_menu.pack(fill="both", expand="yes")

        ######################################################################
        #                         Mode Generation
        ######################################################################

        frame0 = Frame(subframe_menu)
        frame0.pack(fill="both", expand="yes", ipadx=20, ipady=20)
        subframe_menu.add(frame0, text="Génération")

        frame1 = LabelFrame(frame0, text="Génération de la note", padx=20, pady=20);
        frame1.pack(fill="both", side="left", expand="yes")

        label1 = Label(frame1, text="Générer note ici").pack()

        ###########

        frame2 = LabelFrame(frame0, text="Génération des accords", padx=20, pady=20);
        frame2.pack(fill="both", side="right", expand="yes")

        label2 = Label(frame2, text="Générer accords ici").pack()

        ##########################

        ######################################################################
        #                         Fenêtre Affichage
        ######################################################################

        #frame3 = LabelFrame(root, text="Affichage des notes", padx=20, pady=20);
        #frame3.pack(fill="both", expand="yes")

        #label3 = Label(frame3, text="Affichage ici").pack()

        ######################################################################
        #                          Mode Clavier
        ######################################################################

        frame4 = LabelFrame(subframe_menu, text="Clavier", padx=20, pady=20);
        frame4.pack(fill="both", expand="yes")
        subframe_menu.add(frame0, text="Clavier")

        label4 = Label(frame4, text="Clavier ici").pack()

        root.mainloop()


if __name__ == "__main__":
    app = UI_Main()
