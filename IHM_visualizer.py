from frequencies_view import View
from observer import Subject, Observer

import sys
if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import Tk,Frame
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import Tk,Frame
    from tkinter import filedialog

class NoteSelector(Subject):
    """Note selection widget"""

    def __init__(self):
        super().__init__()
