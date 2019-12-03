from tkinter import Frame,Button
from Utils.signal import Signal

class Keyboard :
    '''piano widget controller'''
    def __init__(self,parent,octavemodel, key_w=50, key_h=220, signalsModel=None) :
        self.parent=parent
        self.model=octavemodel
        self.signalsModel = signalsModel
        self.create_keyboard(key_w, key_h)
    def create_keyboard(self, key_w=50, key_h=220) :
        dx_white,dx_black=0,0
        self.keyboard=Frame(self.parent,borderwidth=5,width=7*key_w,height=key_h,bg="red")
        for key in self.model.gamme.keys() :
            if  key.startswith( '#', 1, len(key) ) :
                delta_w,delta_h=3/4.,2/3.
                delta_x=3/5.
                button=Button(self.keyboard,name=key.lower(),width=3,height=6, bg = "black")
                button.bind("<Button-1>",lambda event,x = key : self.play_note(x))
                button.place(width=key_w*delta_w,height=key_h*delta_h,x=key_w*delta_x+key_w*dx_black,y=0)
                if key.startswith('D#', 0, len(key) ) :
                    dx_black=dx_black+2
                else :
                    dx_black=dx_black+1
            else :
                if key=="D" and self.model.get_degree() == 3 :
                    button=Button(self.keyboard,name=key.lower(),bg = "grey")
                else :
                    button=Button(self.keyboard,name=key.lower(),bg = "white")
                button.bind("<Button-1>",lambda event,x = key : self.play_note(x))
                button.place(width=key_w,height=key_h,x=key_w*dx_white,y=0)
                dx_white=dx_white+1
    def play_note(self,key) :
        if(self.signalsModel):
            note_wavs = self.signalsModel.get_wavs(dirpath="Sounds/", regex="[A-G]#?[0-9].wav")
            for sig in note_wavs.values():
                sig.unset_values()

        if(self.signalsModel):
            try:
                sig = self.signalsModel.note_wavs[("Sounds/", "{0}{1}.wav".format(key, self.model.degree))]
                sig.generate()
            except KeyError:
                pass
        self.model.piano_key(key)

    def get_keyboard(self) :
        return self.keyboard
    def get_degrees(self) :
        return self.degrees
