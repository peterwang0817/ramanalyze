import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from frames import DataPathSelectionFrame, PlotConfigurationFrame, PlotVisualizationFrame, FitOverviewFrame
import numpy as np

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
        self.df = []

        self.create_subframes()
        self.update_plot()


    def callback(self, var, index, mode):

        # Called whenever a variable is changed.

        self.config['axis_type'] = self.plotconfig_frame.get_axis_type()
        self.update_plot()
        return True
    

    def load_data(self, rawdata_path, background_path):

        # Called whenever the load button is pressed.
        self.df = []#pd.DataFrame(columns=self.df.columns) # clear the dataframe
        
        # Load background data into dataframe
        try:
            self.df.append(np.loadtxt(background_path, max_rows=2000))#['background'] = np.loadtxt(background_path, max_rows=2000)
        except:
            raise FileNotFoundError
        # TODO: popup dialog

        # Load rest of data into dataframe
        for full_path in rawdata_path.split(' '):
            short_path = full_path.split('/')[-1]
            try:
                self.df.append(np.loadtxt(full_path, max_rows=2000))#[short_path] = np.loadtxt(full_path, max_rows=2000)
            except:
                raise FileNotFoundError
        # TODO: popup dialog

        self.update_plot()


    def create_subframes(self):

        # Basic subroutine to instantiate each of the subframes.

        datapath_frame = DataPathSelectionFrame(self, self.load_data)
        datapath_frame.grid(column=0, row=0)

        self.plotconfig_frame = PlotConfigurationFrame(self)
        self.plotconfig_frame.grid(column=0, row=1)

        self.plot_frame = PlotVisualizationFrame(self)
        self.plot_frame.grid(column=0, row=2, sticky=tk.W)

        testbutton = ttk.Button(self, text='test', command=lambda: print(self.plotconfig_frame.get_axis_type()))
        testbutton.grid(column=1, row=3, sticky=tk.E)

        aaa = FitOverviewFrame(self)
        aaa.grid(column=0, row=4)


    def update_plot(self):

        # Update the plot in the PlotVisualiationFrame.

        self.plot_frame.update_plot(self.config, self.df)


if __name__ == '__main__':

    app = App()

    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
        
    finally:
        app.mainloop()