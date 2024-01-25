from tkinter.simpledialog import askstring
import tkinter as tk
from translation_utils import translate
from database import save_to_database,fetch_expired_words, fetch_words,fetch_all_meanings_from_database, delete_word, get_meaning_by_word, get_meaning_by_word
from mysql.connector import Error
import random

class AppUtils:
    @staticmethod
    def translate_word(entry_word, output_text):
        word_to_translate = entry_word.get()
        translation = translate(word_to_translate)
        translation_result = f"Translation of '{word_to_translate}': {translation}"
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, translation_result)

    @staticmethod
    def change_meaning_and_add_to_learning(entry_word):
        custom_meaning = askstring("Change Meaning", "Enter the desired meaning:")
        if custom_meaning:
            word_to_save = entry_word.get()
            save_to_database(word_to_save, custom_meaning)
            tk.messagebox.showinfo(title="Successful",
                                message=f"The word '{word_to_save}' has been saved with the custom meaning!")

    @staticmethod
    def delete_word(word, show_words_screen_func):
        try:
            delete_word(word)
            tk.messagebox.showinfo(title="Word Deleted", message=f"The word '{word}' has been deleted.")
            show_words_screen_func()
        except Error as e:
            print("Error:", e)

    @staticmethod
    def fetch_all_meanings_except(excluded_meaning):
        all_meanings = fetch_all_meanings_from_database()
        return [meaning for meaning in all_meanings if meaning != excluded_meaning]

    @staticmethod
    def shuffle(listToShuffle):
        # Shuffle the options
        random.shuffle(listToShuffle)
        return listToShuffle

    @staticmethod
    def quiz_words(word_to_practice):
        # Get the correct meaning for the word to practice
        correct_meaning = get_meaning_by_word(word_to_practice)

        # Fetch three random meanings for incorrect options
        all_meanings = AppUtils.fetch_all_meanings_except(correct_meaning)
        incorrect_options = random.sample(all_meanings, min(3, len(all_meanings)))

        # Combine the correct meaning with incorrect options
        options = [correct_meaning] + incorrect_options

        return options

    @staticmethod
    def get_words_to_practice():
        # Fetch and get only words
        words_and_meanings = fetch_words()
        words = [word for word, _ in words_and_meanings]

        # Shuffle the words
        shuffled_words = words.copy()
        random.shuffle(shuffled_words)
        print("shuffled words:", shuffled_words)

        return shuffled_words
    

    @staticmethod
    def check_if_expired():
        expired_words = fetch_expired_words()
        print(expired_words)
        return expired_words

