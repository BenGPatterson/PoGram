# -*- coding: utf-8 -*-

import os
import tkinter as tk
import ctypes
from homepage import HomePage, LoadingPage
from gamepage import GamePage
  
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs): 
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # Window settings
        self.title('PoGram')
        self.base_size = (874, 540)
        self.game_size = (874, 540)
        self.game_fs = 'normal'
        self.geometry(f'{self.base_size[0]}x{self.base_size[1]}')
        self.resizable(False, False)
         
        # Creating a container
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
  
        # Initializing all frame pages
        self.frames = {}
        page_names = ['loading', 'home', 'game']
        page_frames = [LoadingPage, HomePage, GamePage]
        for name, F in zip(page_names, page_frames):
            frame = F(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.current_frame = None
        self.show_frame('loading')

        # Bind resize event to update widgets
        self.bind('<Configure>', self.resize_update)
  
    # Displays chosen page
    def show_frame(self, name):

        # Change window size back to default when leaving game
        if self.current_frame == self.frames['game']:
            self.resizable(False, False)
            self.game_fs = self.wm_state()
            self.wm_state('normal')
            self.game_size = (self.winfo_width(), self.winfo_height())
            self.geometry(f'{self.base_size[0]}x{self.base_size[1]}')

        # Load new frame
        self.current_frame = self.frames[name]
        if name == 'home':
            self.current_frame.menu_frame.play_btn.focus_set()
        elif name == 'game':
            self.resizable(True, True)
            self.wm_state(self.game_fs)
            self.geometry(f'{self.game_size[0]}x{self.game_size[1]}')
        self.current_frame.tkraise()

    # Tell menu frame to load dictionary
    def load_dict(self):
        self.frames['home'].menu_frame.load_dict(os.path.join('PoGram', 'data', 'wiki_entries.pgz'))
        self.show_frame('home')

    # Update game frame widgets after resizing window
    def resize_update(self, event):
        if event.widget == self and self.current_frame == self.frames['game']:
            self.frames['game'].question_frame.q_frame_update()        

# Driver code
if __name__ == '__main__':

    app = tkinterApp()
    if os.name == 'nt':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('PoGram')
    app.iconbitmap(os.path.join('PoGram', 'icon.ico'))
    app.after(250, app.load_dict)
    app.mainloop()