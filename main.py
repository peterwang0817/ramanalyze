import tkinter as tk
from tkinter import ttk

# Basic properties
window_width = 1200
window_height = 800

# Create the tk
root = tk.Tk()
root.title('Ramanalyze')

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print(f'Dimensions of screen: {screen_width}x{screen_height}')

# Find center point of screen
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.iconbitmap('./assets/icon.ico')

# Add message
tk.Label(root, text='Hello world!').pack()
ttk.Label(root, text='Henlo wrold?').pack()

# Main loop
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()