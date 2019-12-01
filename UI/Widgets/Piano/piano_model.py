import collections
from Utils.observer import Subject

class Octave(Subject) :
    '''piano widget model'''
    def __init__(self,degree=3) :
        Subject.__init__(self)
        self.degree=degree
        self.current_key = None
        self.set_gamme(degree)
    def set_gamme(self,degree=3) :
        self.degree=degree
        folder="Sounds"
        notes=["C","D","E","F","G","A","B","C#","D#","F#","G#","A#"]
        self.gamme=collections.OrderedDict()
        for key in notes :
            self.gamme[key]="Sounds/"+key+str(degree)+".wav"
        return self.gamme
    def get_gamme(self) :
        return self.gamme
    def get_degree(self) :
        return self.degree
    def piano_key(self, key):
        self.current_key = key
        self.notify()
        self.current_key = None
    # def notify(self) :
    #     for obs in self.observers:
    #         obs.update(self)
