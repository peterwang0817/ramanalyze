#Import Tkinter library
from tkinter import *
from tkinter import ttk
#Create an instance of Tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
#Set the default value for SpinBox
my_var= StringVar(win)
my_var.set("561")
#Create a spinbox
spinbox= ttk.Spinbox(win, from_=0, to=1000, textvariable=my_var, width=10)
spinbox.pack(ipadx=20, pady=20)
win.mainloop()