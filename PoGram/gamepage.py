import tkinter as tk
import webbrowser

# Game page showing word and questions
class GamePage(tk.Frame):
    def __init__(self, parent, controller): 

        tk.Frame.__init__(self, parent)

        # Grid weights
        self.grid_rowconfigure((0,2), weight=1)
        self.grid_rowconfigure(1, weight=6)
        self.grid_columnconfigure(0, weight=1)

        # Make title panel
        self.title_frame = title_panel(self, controller, bg='#ffffba')
        self.title_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
        
        # Make question panel
        temp = tk.Label(self, text='questions', font=('Segoe UI', 22))
        temp.grid(row=1, column=0)

        # Make next word panel
        temp = tk.Label(self, text='next word', font=('Segoe UI', 12))
        temp.grid(row=2, column=0)

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
        self.word = tk.Label(self, text='dżdżownica', font=('Segoe UI', 22), bg=self.bg)
        self.word.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Make button to open wiktionary for word
        wiki_btn = tk.Button(self, text='wiktionary.org', padx=5, pady=5, command=self.open_wiki)
        wiki_btn.place(relx=0.98, rely=0.5, anchor=tk.E)

    # Exit game and return to home page
    def return_home(self, controller):
        controller.show_frame('home')

    # Open wiktionary page for word
    def open_wiki(self):
        word = self.word['text']
        url = f'https://en.wiktionary.org/wiki/{word}#Polish'
        webbrowser.open(url, new=0, autoraise=True)

        

