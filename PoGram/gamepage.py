import tkinter as tk
import webbrowser
from custom_widgets import Scrollable

# Game page showing word and questions
class GamePage(tk.Frame):
    def __init__(self, parent, controller): 

        tk.Frame.__init__(self, parent)

        # Grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Make title panel
        self.title_frame = title_panel(self, controller, bg='#baffc9')
        self.title_frame.grid(row=0, column=0, ipady=30, sticky='nsew')
        
        # Make question panel
        self.question_frame = question_panel(self, controller)
        self.question_frame.grid(row=1, column=0, sticky='nsew')

# Title panel showing word
class title_panel(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.bg = kwargs.get('bg', self.cget('bg'))

        # Make return button
        return_btn = tk.Button(self, text='Return', padx=5, pady=5, command=lambda: self.return_home(controller))
        return_btn.place(relx=0.02, rely=0.5, anchor=tk.W)

        # Make word label
        self.grid_columnconfigure(1, weight=1)
        self.word = tk.StringVar(value='dżdżownica')
        self.word_lbl = tk.Label(self, textvariable=self.word, font=('Segoe UI', 22), bg=self.bg)
        self.word_lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Make button to open wiktionary for word
        wiki_btn = tk.Button(self, text='wiktionary.org', padx=5, pady=5, command=self.open_wiki)
        wiki_btn.place(relx=0.98, rely=0.5, anchor=tk.E)

    # Exit game and return to home page
    def return_home(self, controller):
        controller.show_frame('home')

    # Open wiktionary page for word
    def open_wiki(self):
        word = str(self.word.get())
        url = f'https://en.wiktionary.org/wiki/{word}#Polish'
        webbrowser.open(url, new=0, autoraise=True)

# Question panel showing questions
class question_panel(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller

        # Grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create scrollable frame
        self.count = 0
        self.q_frame = Scrollable(self, width=20)

    # Updates question panel after widget added
    def q_frame_update(self):
        self.q_frame.update()
        free_space = self.controller.winfo_height() - self.q_frame.winfo_height()\
                     - self.parent.title_frame.word_lbl.winfo_height() - 2*self.parent.title_frame.grid_info()['ipady']
        pad_amount = max(0, int(free_space/2))
        self.q_frame.canvas.grid_configure(pady=(pad_amount,0))


        

    

        

