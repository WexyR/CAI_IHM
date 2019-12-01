import os
import subprocess

from tkinter import Frame,Button,Label
from Utils.observer import Observer

class Screen(Observer):
    '''piano widget view'''
    def __init__(self,parent) :
        self.parent=parent
        self.create_screen()
    def create_screen(self) :
        self.screen=Frame(self.parent,borderwidth=5,width=500,height=160,bg="pink")
        self.info=Label(self.screen,text="Appuyez sur une touche clavier ", bg="pink",font=('Arial',10))
        self.info.pack()
    def get_screen(self) :
        return self.screen
    def update(self,model,key="C") :
        if __debug__:
            if key not in model.gamme.keys()  :
                raise AssertionError
        if(os.path.exists(model.get_gamme()[key])):
            subprocess.call(["aplay", model.get_gamme()[key]])
        else:
            print("Le fichier "+model.get_gamme()[key]+" n'est pas généré.")
        if self.info :
            self.info.config(text = "Vous avez joué la note : " + key + str(model.get_degree()))
