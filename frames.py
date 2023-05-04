import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import StringVar, DoubleVar

import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

import numpy as np
from classes import Series
import curves as cv

HC = 1239.841930092394
options = {'padx': 5, 'pady': 5}

class DataPathSelectionFrame(ttk.Frame):

    # Contains 2 selection boxes to choose rawdata path and background path.

    def __init__(self, container, load_data_callback):

        super().__init__(container)

        # field options

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

        self.figure = Figure(figsize=(5, 4), dpi=120)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        NavigationToolbar2Tk(self.figure_canvas, self)
        self.axes = self.figure.add_subplot()
        self.axes.set_ylabel("counts")
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def update_plot(self, config, df, target_func, guess):
        
        # Called when a variable is changed, or when instantiated. 'config' is expected to be the global config variable from the root window.

        self.axes.clear()

        # Set title
        self.axes.set_title(config['plot_title'])

        # Set x axis
        if config['axis_type'] == 'wavelength': self.axes.set_xlabel('Wavelength (nm)')
        elif config['axis_type'] == 'energy': self.axes.set_xlabel('Energy (eV)')
        elif config['axis_type'] == 'ramanshift': self.axes.set_xlabel('Raman shift (cm⁻¹)')
        else: self.axes.set_xlabel('This isnt supposed to be here')
        
        if len(df) > 0:
            
            x_axis = df[0][:,0]
            if config['axis_type'] == 'energy':
                x_axis = np.reciprocal(x_axis) * HC
            elif config['axis_type'] == 'ramanshift':
                x_axis = 1E7 * (1.0 / float(config['exc_wavelength']) - np.reciprocal(x_axis))

            for i, v in enumerate(df[1:]):
                self.axes.plot(x_axis, v[:,1])# - df[0][:,1])
                foo = Series('1', x_axis, v[:,1], None, 'blue')
                #bar = foo.fit(target_func, guess)
                #self.axes.plot(x_axis, bar.ydata)

        self.figure_canvas.draw_idle()
        self.figure_canvas.flush_events()
        # I don't know how to use matplotlib


class NewPlotVisualizationFrame(tk.Frame):

    # Frame used to integrate matplotlib into tkinter.

    def __init__(self, container, axis_type):

        super().__init__(container)

        # Create a figure
        self.figure = Figure(figsize=(5, 4), dpi=120)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)
        # Create navigation bar
        NavigationToolbar2Tk(self.figure_canvas, self)
        self.axes = self.figure.add_subplot()
        # Set x axis
        self.axis_type = axis_type
        if self.axis_type == 'energy':
            self.axes.set_xlabel('Energy (eV)')
        elif self.axis_type == 'ramanshift':
            self.axes.set_xlabel('Raman shift (cm⁻¹)')
        else:
            self.axes.set_xlabel('Wavelength (nm)')
        # Set y axis
        self.axes.set_ylabel("counts")
        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def update_plot(self, config, df):
        
        # Called when a variable is changed, or when instantiated. 'config' is expected to be the global config variable from the root window.

        self.axes.clear()

        # Set title
        self.axes.set_title(config['plot_title'])
        
        if len(df) > 0:
            
            x_axis = df[0][:,0]
            if self.axis_type == 'energy':
                x_axis = np.reciprocal(x_axis) * HC
            elif self.axis_type == 'ramanshift':
                x_axis = 1E7 * (1.0 / float(config['exc_wavelength']) - np.reciprocal(x_axis))

            for i, v in enumerate(df[1:]):
                self.axes.plot(x_axis, v[:,1])# - df[0][:,1])
                foo = Series(str(i), x_axis, v[:,1], None, 'blue')
                #bar = foo.fit(gaussian)
                #self.axes.plot(x_axis, bar.ydata)

        self.figure_canvas.draw_idle()
        self.figure_canvas.flush_events()
        # I don't know how to use matplotlib

class FitParameterFrame(tk.Frame):

    def __init__(self, container):

        super().__init__(container)

        self.name = StringVar()
        self.type = StringVar()
        self.a = DoubleVar()
        self.b = DoubleVar()
        self.c = DoubleVar()
        self.a.set(1)
        self.b.set(1)
        self.c.set(1)

        curve_names = ('Gaussian', 'Lorentz')

        name_label = ttk.Label(self, text='Name')
        name_label.grid(column=0, row=0, padx=5)
        name_entry = ttk.Entry(self, textvariable=self.name, width=10)
        name_entry.grid(column=1, row=0)

        type_entry = ttk.OptionMenu(self, self.type, curve_names[1], *curve_names)
        type_entry.configure(width=8)
        type_entry.grid(column=2, row=0)

        a_label = ttk.Label(self, text='a')
        a_label.grid(column=3, row=0, padx=5)
        a_entry = ttk.Entry(self, textvariable=self.a, width=6)
        a_entry.grid(column=4, row=0)

        b_label = ttk.Label(self, text='b')
        b_label.grid(column=5, row=0, padx=5)
        b_entry = ttk.Entry(self, textvariable=self.b, width=6)
        b_entry.grid(column=6, row=0)

        c_label = ttk.Label(self, text='c')
        c_label.grid(column=7, row=0, padx=5)
        c_entry = ttk.Entry(self, textvariable=self.c, width=6)
        c_entry.grid(column=8, row=0)

        remove_button = ttk.Button(self, text='Remove', command=self.commit_die)
        remove_button.grid(column=9, row=0, padx=5)

    def commit_die(self):

        self.destroy()

    def get_params(self):

        return (self.name.get(), self.type.get(), self.a.get(), self.b.get(), self.c.get())
    

class FitOverviewFrame(tk.Frame):

    def __init__(self, container):

        super().__init__(container)
        self.younglings = []

        add_button = ttk.Button(self, text='add new curve', command=self.on_pressed)
        add_button.grid(column=0, row=0, sticky=tk.N)

        test = ttk.Button(self, text='bam', command=self.get_all_params)
        test.grid(column=1, row=0)


    def on_pressed(self):

        new_curve = FitParameterFrame(self)
        new_curve.grid(column=0, columnspan=2)


    def get_all_params(self):
        
        all_params = []
        #print('\nViewing children:\n')

        for key in self.children:

            if '!button' not in key:

                #print(f'Key: {key}\nValue: {self.children[key].get_params()}')
                for param in self.children[key].get_params()[2:]:
                    all_params.append(param)

        return all_params
    
    def get_fit_function(self):
        
        funcs = []

        for key in self.children:

            if '!button' not in key:

                name = self.children[key].get_params()[1]
                if name == 'Gaussian':
                    funcs.append(cv.gaussian)
                elif name == 'Lorentz':
                    funcs.append(cv.lorentzian)

        return lambda x, *args: sum(f(x, *args[3*i:3*i+3]) for i, f in enumerate(funcs))