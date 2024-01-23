import tkinter as tk
from app_utils import AppUtils

class GUIUtils:
    @staticmethod
    def create_menubar(root, translation_screen_func, show_words_screen_func, quiz_words_func):
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        open_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Open", menu=open_menu)

        open_menu.add_command(label="Translate a Word", command=translation_screen_func)
        open_menu.add_command(label="Show Words", command=show_words_screen_func)

        practice_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Practice", menu=practice_menu)

        practice_menu.add_command(label="Quiz Words", command=quiz_words_func)
