import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import StringVar
from tkinter import IntVar

class AxisSelectorFrame(ttk.Frame):

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

        x_axis = StringVar(self.master)
        x_axis.set('wavelength')
        exc_wavelength = StringVar(self.master)
        exc_wavelength.set('561')

        # Title
        ttk.Label(self, text='Horizontal axis').grid(column=0, row=0, columnspan=4, **options)

        # X-axis units (nm / eV / cm^-1)
        wavelength = ttk.Radiobutton(self, text='Wavelength (nm)', variable=x_axis, value='wavelength')
        wavelength.grid(column=0, row=1, sticky=tk.W, **options)

        energy = ttk.Radiobutton(self, text='Photon energy (eV)', variable=x_axis, value='energy')
        energy.grid(column=0, row=2, sticky=tk.W, **options)

        ramanshift = ttk.Radiobutton(self, text='Raman shift (cm⁻¹)', variable=x_axis, value='ramanshift')
        ramanshift.grid(column=0, row=3, sticky=tk.W, **options)

        # Excitation wavelength
        exc_label = ttk.Label(self, text='Excitation wavelength')
        exc_label.grid(column=2, row=1, columnspan=2, **options)

        exc_spinbox = ttk.Spinbox(self, from_=0, to=1000, textvariable=exc_wavelength, width=10)
        exc_spinbox.grid(column=2, row=2, sticky=tk.E, **options)
        ttk.Label(self, text='nm').grid(column=3, row=2, sticky=tk.W, **options)



class ConfigurationFrame(ttk.Frame):

    def __init__(self, container):

        super().__init__(container)

        # field options
        options = {'padx': 5, 'pady': 5}

        # Configure columns
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=4)
        self.columnconfigure(index=2, weight=1)

        rawdata = StringVar()
        background = StringVar()

        # Choose files
        rawdata_label = ttk.Label(self, text='Raw data:')
        rawdata_label.grid(column=0, row=0, sticky=tk.W, **options)

        rawdata_entry = ttk.Entry(self, textvariable=rawdata, width=140)
        rawdata_entry.grid(column=1, row=0, **options)

        rawdata_button = ttk.Button(self, text='Choose file', command=lambda: self.choose_file(rawdata_entry, multi=True))
        rawdata_button.grid(column=2, row=0, sticky=tk.E, **options)

        # Choose background
        background_label = ttk.Label(self, text='Background:')
        background_label.grid(column=0, row=1, sticky=tk.W, **options)

        background_entry = ttk.Entry(self, textvariable=background, width=140)
        background_entry.grid(column=1, row=1, **options)

        background_button = ttk.Button(self, text='Choose file', command=lambda: self.choose_file(background_entry))
        background_button.grid(column=2, row=1, sticky=tk.E, **options)

        # Choose something
        mode_selector = AxisSelectorFrame(self)
        mode_selector.grid(column=0, row=2, columnspan=2, sticky=tk.W, **options)


    def choose_file(self, entry_box, multi=False):

        entry_box.delete(0, tk.END)

        if multi:
            filename = fd.askopenfilenames()
            entry_box.insert(0, filename)
        else:
            filename = fd.askopenfilename()
            entry_box.insert(0, filename)
