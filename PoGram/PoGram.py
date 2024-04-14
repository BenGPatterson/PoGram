# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import font
from pl_chars import Entry_pl

LARGEFONT=("Verdana", 35)
  
class tkinterApp(tk.Tk):
     
    # __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # Window settings
        self.title("PoGram")
        self.geometry('874x540')
         
        # Creating a container
        container = tk.Frame(self)  
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
  
        # Initializing all frame pages
        self.frames = {}  
        for F in (HomePage, Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky ="nsew")
        self.show_frame(HomePage)
  
    # Displays chosen page
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Home page showing trainer settings
class HomePage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        # Frame weights
        self.grid_rowconfigure(1, weight = 1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight = 1, uniform="column")

        # Title
        title = tk.Label(self, text="PoGram", font=LARGEFONT)
        title.grid(row=0, column=0, columnspan=5, padx=10, pady=0, sticky='nw')
        
        # Trainer frames
        tframe_1 = tk.Frame(self, bg='grey')
        tframe_1.grid(row=1, column=0, padx=10, pady=(10, 20), sticky='nsew')
        tframe_2 = tk.Frame(self, bg='grey')
        tframe_2.grid(row=1, column=1, padx=10, pady=(10, 20), sticky='nsew')
        tframe_3 = tk.Frame(self, bg='grey')
        tframe_3.grid(row=1, column=2, padx=10, pady=(10, 20), sticky='nsew')
        tframe_4 = tk.Frame(self, bg='grey')
        tframe_4.grid(row=1, column=3, padx=10, pady=(10, 20), sticky='nsew')
        menu_frame = tk.Frame(self, bg='grey')
        menu_frame.grid(row=1, column=4, padx=10, pady=(10, 20), sticky='nsew')

        # Adjective trainer settings
        tframe_3.grid_columnconfigure(0, weight = 1)
        adj_active = tk.IntVar()
        adj_toggle = tk.Checkbutton(tframe_3, variable=adj_active, onvalue=1, offvalue=0, bg='grey')
        adj_toggle.grid(row=0, column=0)
        adj_label = tk.Label(tframe_3, text='Adjectives', bg='grey')
        adj_label.grid(row=1, column=0)

          
  
  
# second window frame page1 
class Page1(tk.Frame):
     
    def __init__(self, parent, controller):
         
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text ="Page 1", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = tk.Button(self, text ="StartPage",
                            command = lambda : controller.show_frame(HomePage))
     
        # putting the button in its place 
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button2 = tk.Button(self, text ="Page 2",
                            command = lambda : controller.show_frame(Page2))
     
        # putting the button in its place by 
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
  
  
  
# third window frame page2
class Page2(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text ="Page 2", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = tk.Button(self, text ="Page 1",
                            command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by 
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 3 with text
        # layout3
        button2 = tk.Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(HomePage))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)
  
  
# Driver Code
app = tkinterApp()
app.mainloop()