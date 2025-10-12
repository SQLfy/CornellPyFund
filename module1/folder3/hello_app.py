"""
A Hello World GUI.

The purpose of this App is to test that tkinter is working correctly.

Author: Walker M. White (wmw2)
Date:   July 31, 2018
"""
from tkinter import *


def create_app():
    """
    Returns a Tkinter app not yet executing.
    
    Call mainloop on the app to have it execute.
    """
    root = Tk()
    root.title('Hello App')
    root.protocol("WM_DELETE_WINDOW",root.quit)
    
    mssg = Label(root, text="Hello World!", font=("Times", 44))
    mssg.pack()
    return root


if __name__ == '__main__':
    create_app().mainloop()