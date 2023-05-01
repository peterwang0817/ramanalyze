import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from frames import ConfigurationFrame, AxisSelectorFrame

# Basic properties
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

class App(tk.Tk):

    def __init__(self):

        super().__init__()

        # Window title
        self.title('Ramanalyze')
        
        # Dimensions and position of window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - WINDOW_WIDTH / 2)
        center_y = int(screen_height/2 - WINDOW_HEIGHT / 2)
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}')

        # Configure icon
        self.iconbitmap('./assets/icon.ico')

        self.create_widgets()


    def create_widgets(self):

        frame = ConfigurationFrame(self)
        frame.pack()


if __name__ == '__main__':
    app = App()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        app.mainloop()