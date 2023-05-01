import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import StringVar

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

        rawdata_entry = ttk.Entry(self, textvariable=rawdata)
        rawdata_entry.grid(column=1, row=0, **options)

        rawdata_button = ttk.Button(self, text='Choose file', command=lambda: self.choose_file(rawdata_entry, multi=True))
        rawdata_button.grid(column=2, row=0, sticky=tk.E, **options)

        # Choose background
        background_label = ttk.Label(self, text='Background:')
        background_label.grid(column=0, row=1, sticky=tk.W, **options)

        background_entry = ttk.Entry(self, textvariable=background)
        background_entry.grid(column=1, row=1, **options)

        background_button = ttk.Button(self, text='Choose file', command=lambda: self.choose_file(background_entry))
        background_button.grid(column=2, row=1, sticky=tk.E, **options)


    def choose_file(self, entry_box, multi=False):

        entry_box.delete(0, tk.END)

        if multi:
            filename = fd.askopenfilenames()
            entry_box.insert(0, filename)
        else:
            filename = fd.askopenfilename()
            entry_box.insert(0, filename)
