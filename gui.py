import tkinter as tk
from gui_utils import GUIUtils
from app_utils import AppUtils
from translation_utils import translate
from database import save_to_database, fetch_words, get_meaning_by_word
from mysql.connector import Error
from tkinter.simpledialog import askstring
from tkinter import messagebox

class LanguageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Learning App")
        self.root.geometry("800x400")
        GUIUtils.create_menubar(root, self.translation_screen, self.show_words_screen, self.quiz_screen)
        self.translation_screen()
        self.expired_words = AppUtils.check_if_expired()
        

    def translation_screen(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=50)

        label = tk.Label(frame, text="Enter a Word:")
        label.grid(row=0, column=0)

        self.entry_word = tk.Entry(frame, width=50)
        self.entry_word.grid(row=0, column=1)

        translate_button = tk.Button(frame,
                                    text="Translate",
                                    command=lambda: AppUtils.translate_word(self.entry_word, self.output_text),
                                    width=10,
                                    height=2,
                                    padx=10
                                    )
        translate_button.grid(row=0, column=2)

        output_frame = tk.Frame(self.root, bg="white")
        output_frame.pack(pady=20)

        self.output_text = tk.Text(output_frame, wrap=tk.WORD, width=50, height=5)
        self.output_text.pack()

        add_to_learnings_button = tk.Button(
            self.root,
            text="Add to Learnings!",
            command=lambda: AppUtils.save_word_to_learning(self.entry_word),
            width=15,
            height=2,
            padx=10
        )
        add_to_learnings_button.pack(side="left", padx=5)

        change_meaning_button = tk.Button(
            self.root,
            text="Change Meaning",
            command=lambda: AppUtils.change_meaning_and_add_to_learning(self.entry_word),
            width=15,
            height=2,
            padx=10
        )
        change_meaning_button.pack(side="left", padx=5)

    def show_words_screen(self):
        # Create show words screen GUI
        show_words_frame = tk.Toplevel(self.root)
        show_words_frame.title("Show Words")
        show_words_frame.geometry("800x600")  # Set the desired width and height

        whiteboard_frame = tk.Frame(show_words_frame, bg="white", height=500)  # Set the desired height
        whiteboard_frame.pack(pady=20)

        canvas = tk.Canvas(whiteboard_frame, bg="white", height=500, width=245)  # Set the desired width
        canvas.pack(side="left", fill="both", expand=True)

        myscrollbar = tk.Scrollbar(whiteboard_frame, orient="vertical", command=canvas.yview)
        myscrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=myscrollbar.set)

        # Fetch words and meanings from the database
        words_and_meanings = fetch_words()

        for i, (word, meaning) in enumerate(words_and_meanings):
            label_text = f"{word} -> {meaning}"
            label = tk.Label(canvas, text=label_text, anchor="w", padx=3, bg="white")
            canvas.create_window((0, i * 30), window=label, anchor="nw")

            delete_button = tk.Button(canvas, text="Delete", command=lambda w=word: AppUtils.delete_word(w, self.show_words_screen))
            canvas.create_window((200, i * 30), window=delete_button, anchor="nw")

        num_of_words_text = f"Number of words you're currently learning: {len(words_and_meanings)}"
        num_of_words = tk.Label(show_words_frame, text=num_of_words_text)
        num_of_words.pack()
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

    def quiz_screen(self):
        self.wordsToPractice = AppUtils.get_words_to_practice()
        i = 0

        # Create a new quiz window
        quiz_window = tk.Toplevel(self.root)
        quiz_window.title("Quiz")
        quiz_window.geometry("600x200")

        def ask_question():
            nonlocal i
            # Call quiz_words to get the word to practice and options
            word_to_practice = self.wordsToPractice[i]
            options = AppUtils.quiz_words(word_to_practice)
            print("w t p:", word_to_practice)

            # Display the question
            question_label = tk.Label(quiz_window, text=f"Which of the following is the meaning of the word '{word_to_practice}'?")
            question_label.pack(pady=10)

            # Shuffle the options for randomness
            random_options = AppUtils.shuffle_options(options)

            # Create buttons for each option
            for option in random_options:
                button = tk.Button(quiz_window, text=option, command=lambda o=option: self.check_answer(o, word_to_practice, quiz_window))
                button.pack(pady=5)

            # Wait for the user to answer before moving to the next question
            quiz_window.wait_window()

            # Clear the question and options for the next round
            question_label.destroy()
            for widget in quiz_window.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.destroy()

            # Increment to the next word
            i += 1

            # Check if there are more words to practice
            if i < len(self.wordsToPractice):
                # After a delay (you can adjust this), ask the next question
                quiz_window.after(2000, ask_question)
            else:
                # If there are no more words, close the quiz window
                quiz_window.destroy()

        # Start asking the first question
        ask_question()



    
    def check_answer(self, selected_option, correct_word, quiz_window):
        if selected_option == get_meaning_by_word(correct_word):
            messagebox.showinfo("Correct", "Congratulations! You selected the correct answer.")
        else:
            correct_meaning = get_meaning_by_word(correct_word)
            messagebox.showerror("Incorrect", f"Sorry, the correct answer is: {correct_meaning}")

        # Clear the previous question and options
        for widget in quiz_window.winfo_children():
            widget.destroy()

        # Call quiz_words to get the word to practice and options
        options = AppUtils.quiz_words(correct_word)

        # Display the next question
        question_label = tk.Label(quiz_window, text=f"Which of the following is the meaning of the word '{correct_word}'?")
        question_label.pack(pady=10)

        # Shuffle the options for randomness
        random_options = AppUtils.shuffle_options(options)

        # Create buttons for each option
        for option in random_options:
            button = tk.Button(quiz_window,
                               text=option,
                               command=lambda o=option: self.check_answer(o, correct_word, quiz_window))
            button.pack(pady=5)

