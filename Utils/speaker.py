import subprocess
import os

from Utils.observer import *

class Speaker(Observer):
    def __init__(self):
        super().__init__()

    def update(self, sig):
        print(sig)
        if(sig.isplaying):
            if(os.path.exists("Sounds/"+sig.wavname)):
                print("test")
                subprocess.call(["aplay", "Sounds/"+sig.wavname])
