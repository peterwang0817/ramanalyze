import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from frames import DataPathSelectionFrame, PlotConfigurationFrame, PlotVisualizationFrame

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

        # Global variables
        self.config = {'axis_type':         'wavelength',
                       'exc_wavelength':    '561',
                       'plot_title':        'Spectrum',
                       }

        self.create_subframes()
        self.update_plot()


    def callback(self, var, index, mode):

        # Called whenever a variable is changed.

        self.config['axis_type'] = self.plotconfig_frame.get_axis_type()
        self.update_plot()
        return True

    def create_subframes(self):

        # Basic subroutine to instantiate each of the subframes.

        datapath_frame = DataPathSelectionFrame(self)
        datapath_frame.pack()

        self.plotconfig_frame = PlotConfigurationFrame(self)
        self.plotconfig_frame.pack()

        self.plot_frame = PlotVisualizationFrame(self)
        self.plot_frame.pack()

        testbutton = ttk.Button(self, text='test', command=lambda: print(self.plotconfig_frame.get_axis_type()))
        testbutton.pack()


    def update_plot(self):

        # Update the plot in the PlotVisualiationFrame.

        self.plot_frame.update_plot(self.config)


if __name__ == '__main__':

    app = App()

    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
        
    finally:
        app.mainloop()