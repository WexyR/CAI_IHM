import sys
if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import Tk,Frame,Button,Label,LabelFrame,Frame
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import Tk,Frame,Button,Label,LabelFrame
    from tkinter import filedialog

if __name__ == "__main__":
    root = Tk()
    root.geometry("600x350")
    root.title("La leçon de piano - Beta Version - Do not distribute")

    ######################################################################
    #                           Generation
    ######################################################################

    frame0 = Frame(root)
    frame0.pack(fill="both", expand="yes", ipadx=20, ipady=20)
    frame1 = LabelFrame(frame0, text="Génération de la note", padx=20, pady=20);
    frame1.pack(fill="both", side="left", expand="yes")

    label1 = Label(frame1, text="Générer note ici").pack()

    ######################################################################
    #                           Combinaison
    ######################################################################

    frame2 = LabelFrame(frame0, text="Génération des accords", padx=20, pady=20);
    frame2.pack(fill="both", side="right", expand="yes")

    label2 = Label(frame2, text="Générer accords ici").pack()

    ######################################################################
    #                           Affichage
    ######################################################################

    frame3 = LabelFrame(root, text="Affichage des notes", padx=20, pady=20);
    frame3.pack(fill="both", expand="yes")

    label3 = Label(frame3, text="Affichage ici").pack()

    ######################################################################
    #                           Piano
    ######################################################################

    frame4 = LabelFrame(root, text="Clavier", padx=20, pady=20);
    frame4.pack(fill="both", expand="yes")

    label4 = Label(frame4, text="Clavier ici").pack()

    root.mainloop()
