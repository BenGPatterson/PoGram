# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as tkFont
from homepage import HomePage
  
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # Window settings
        self.title('PoGram')
        self.geometry('874x540')
         
        # Creating a container
        container = tk.Frame(self)  
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
  
        # Initializing all frame pages
        self.frames = {}  
        for F in [HomePage]:
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(HomePage)
  
    # Displays chosen page
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Driver Code
if __name__ == '__main__':
    app = tkinterApp()
    app.mainloop()