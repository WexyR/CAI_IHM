import subprocess
import os

from Utils.observer import *
from Utils.chord import *

class Speaker(Observer):
    def __init__(self):
        super().__init__()

    def update(self, sig):
        print(sig)
        if(sig.isplaying):
            if(os.path.exists("Sounds/"+"Chords/"*isinstance(sig, Chord)+sig.wavname)):
                subprocess.call(["aplay", "Sounds/"+"Chords/"*isinstance(sig, Chord)+sig.wavname])
