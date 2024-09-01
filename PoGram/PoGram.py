# -*- coding: utf-8 -*-

import os
import tkinter as tk
from homepage import HomePage, LoadingPage
  
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs): 
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # Window settings
        self.title('PoGram')
        self.geometry('874x540')
        self.resizable(False,False)
         
        # Creating a container
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
  
        # Initializing all frame pages
        self.frames = {}
        page_names = ['loading', 'home']
        page_frames = [LoadingPage, HomePage]
        for name, F in zip(page_names, page_frames):
            frame = F(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame('loading')
  
    # Displays chosen page
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    # Tell menu frame to load dictionary
    def load_dict(self):
        self.frames['home'].menu_frame.load_dict(os.path.join('data', 'wiki_entries.pgz'))
        self.show_frame('home')
        # app.unbind('<Visibility>')

# Driver Code
if __name__ == '__main__':

    app = tkinterApp()
    app.after(250, app.load_dict)
    app.mainloop()