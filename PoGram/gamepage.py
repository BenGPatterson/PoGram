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

        # Left button frame
        self.left_button_frame = tk.Frame(self, bg=self.bg)
        self.left_button_frame.place(relx=0.02, rely=0.5, width=150, relheight=0.6, anchor=tk.W)

        # Make return button
        return_btn = tk.Button(self.left_button_frame, text='Return', command=lambda: self.return_home(controller))
        return_btn.place(relx=0, rely=0.5, relwidth=0.5, relheight=1, anchor=tk.W)

        # Make resize window to default button
        reset_btn = tk.Button(self.left_button_frame, text='Reset Size', padx=5, pady=5, command=lambda: self.reset_size(controller))
        reset_btn.place(relx=1, rely=0.5, relwidth=0.5, relheight=1, anchor=tk.E)

        # Make word label
        self.grid_columnconfigure(1, weight=1)
        self.word = tk.StringVar(value='dżdżownica')
        self.word_lbl = tk.Label(self, textvariable=self.word, font=('Segoe UI', 22), bg=self.bg)
        self.word_lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Left button frame
        self.right_button_frame = tk.Frame(self, bg=self.bg)
        self.right_button_frame.place(relx=0.98, rely=0.5, width=150, relheight=0.6, anchor=tk.E)

        # Make button to open wiktionary for word
        wiki_btn = tk.Button(self.right_button_frame, text='Open wiktionary page', padx=5, pady=5, command=self.open_wiki)
        wiki_btn.place(relx=0, rely=0.5, relwidth=1, relheight=1, anchor=tk.W)

    # Exit game and return to home page
    def return_home(self, controller):
        controller.show_frame('home')

    # Reset window size to default
    def reset_size(self, controller):
        controller.game_fs = 'normal'
        controller.game_size = (controller.base_size[0], controller.base_size[1])
        controller.wm_state('normal')
        controller.geometry(f'{controller.base_size[0]}x{controller.base_size[1]}')

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

        # Update y position of question panel
        self.q_frame.update()
        lower_pad = 10
        free_space = self.controller.winfo_height() - self.q_frame.winfo_height()\
                     - self.parent.title_frame.word_lbl.winfo_height() - 2*self.parent.title_frame.grid_info()['ipady']\
                     - lower_pad
        pad_amount = max(0, int(free_space/2))
        self.q_frame.canvas.grid_configure(pady=(pad_amount, lower_pad))

        # Update definition label wraplength
        for widget in self.q_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(wraplength=self.q_frame.winfo_width()-50)