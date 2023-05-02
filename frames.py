import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import StringVar

import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

import pandas as pd

class DataPathSelectionFrame(ttk.Frame):

    # Contains 2 selection boxes to choose rawdata path and background path.

    def __init__(self, container, load_data_callback):

        super().__init__(container)

        # field options
        options = {'padx': 5, 'pady': 5}

        # Configure columns
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=4)
        self.columnconfigure(index=2, weight=1)
        self.columnconfigure(index=3, weight=1)

        self.rawdata_path = StringVar()
        self.background_path = StringVar()

        # Choose files
        rawdata_label = ttk.Label(self, text='Raw data:')
        rawdata_label.grid(column=0, row=0, sticky=tk.W, **options)

        rawdata_entry = ttk.Entry(self, textvariable=self.rawdata_path, width=140)
        rawdata_entry.grid(column=1, row=0, **options)

        rawdata_button = ttk.Button(self, text='Choose file', command=lambda: self.choose_file(rawdata_entry, multi=True))
        rawdata_button.grid(column=2, row=0, sticky=tk.E, **options)

        # Choose background
        background_label = ttk.Label(self, text='Background:')
        background_label.grid(column=0, row=1, sticky=tk.W, **options)

        background_entry = ttk.Entry(self, textvariable=self.background_path, width=140)
        background_entry.grid(column=1, row=1, **options)

        background_button = ttk.Button(self, text='Choose file', command=lambda: self.choose_file(background_entry))
        background_button.grid(column=2, row=1, sticky=tk.E, **options)

        # Load into memory button
        fr = ttk.Frame(self)
        fr.grid(column=3, row=0, rowspan=2, **options)
        load_button = ttk.Button(fr, text='\nLoad\n', command=lambda: load_data_callback(self.rawdata_path.get(), self.background_path.get()))
        load_button.pack()#.grid(column=3, row=0, rowspan=2, **options)


    def choose_file(self, entry_box, multi=False):

        entry_box.delete(0, tk.END)

        if multi:
            filename = fd.askopenfilenames()
            entry_box.insert(0, filename)
        else:
            filename = fd.askopenfilename()
            entry_box.insert(0, filename)


    def get_file_paths(self):

        return self.rawdata_path.get()
    

    def get_background_path(self):

        return self.background_path.get()



class PlotConfigurationFrame(ttk.Frame):

    # Some parameters needed for plotting. Includes:
    # x_axis:           The horizontal axis for plotting. Three modes are available: wavelength, photon energy, and raman shift.
    # exc_wavelength:   Excitation wavelength. This value will be used to fit a Gaussian and fit the exact excitation wavelength.

    def __init__(self, container):

        super().__init__(container)

        # field options
        options = {'padx': 1, 'pady': 1}

        # Configure columns
        self['borderwidth'] = 2
        self['relief'] = 'groove'
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)
        self.columnconfigure(index=3, weight=1)

        self.x_axis = StringVar()
        self.x_axis.set('wavelength')
        self.x_axis.trace_add('write', container.callback)
        # This variable will callback if changed!

        self.exc_wavelength = StringVar()
        self.exc_wavelength.set('561')

        # Title
        ttk.Label(self, text='Horizontal axis').grid(column=0, row=0, columnspan=4, **options)

        # X-axis units (nm / eV / cm^-1) configuration
        wavelength = ttk.Radiobutton(self, text='Wavelength (nm)', variable=self.x_axis, value='wavelength')
        wavelength.grid(column=0, row=1, sticky=tk.W, **options)

        energy = ttk.Radiobutton(self, text='Photon energy (eV)', variable=self.x_axis, value='energy')
        energy.grid(column=0, row=2, sticky=tk.W, **options)

        ramanshift = ttk.Radiobutton(self, text='Raman shift (cm⁻¹)', variable=self.x_axis, value='ramanshift')
        ramanshift.grid(column=0, row=3, sticky=tk.W, **options)

        # Excitation wavelength configuration
        exc_label = ttk.Label(self, text='Excitation wavelength')
        exc_label.grid(column=2, row=1, columnspan=2, **options)

        exc_spinbox = ttk.Spinbox(self, from_=0, to=1000, textvariable=self.exc_wavelength, width=10)
        exc_spinbox.grid(column=2, row=2, sticky=tk.E, **options)
        ttk.Label(self, text='nm').grid(column=3, row=2, sticky=tk.W, **options)


    def callback(self, var, index, mode):
        # unused?
        print(f'{self.x_axis.get()}')
        return True


    def get_axis_type(self):

        return self.x_axis.get()
    

    def get_exc_wavelength(self):

        return self.exc_wavelength.get()
    

class PlotVisualizationFrame(tk.Frame):

    # Frame used to integrate matplotlib into tkinter.

    def __init__(self, container):

        super().__init__(container)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        NavigationToolbar2Tk(self.figure_canvas, self)
        self.axes = self.figure.add_subplot()
        self.axes.set_ylabel("counts")
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def update_plot(self, config, df):
        
        # Called when a variable is changed, or when instantiated. 'config' is expected to be the global config variable from the root window.

        self.axes.clear()

        # Set title
        self.axes.set_title(config['plot_title'])

        # Set x axis
        if config['axis_type'] == 'wavelength': self.axes.set_xlabel('Wavelength (nm)')
        elif config['axis_type'] == 'energy': self.axes.set_xlabel('Energy (eV)')
        elif config['axis_type'] == 'ramanshift': self.axes.set_xlabel('Raman shift (cm⁻¹)')
        else: self.axes.set_xlabel('This isnt supposed to be here')
        
        self.axes.plot(df)

        self.figure_canvas.draw_idle()
        self.figure_canvas.flush_events()
        # I don't know how to use matplotlib

