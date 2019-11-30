from tkinter import Frame,Button

class Keyboard :
    '''piano widget controller'''
    def __init__(self,parent,model, key_w=50, key_h=220) :
        self.parent=parent
        self.model=model
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
        self.model.notify(key)
    def get_keyboard(self) :
        return self.keyboard
    def get_degrees(self) :
        return self.degrees
