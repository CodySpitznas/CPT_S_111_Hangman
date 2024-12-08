import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# Define themes and their corresponding word lists with descriptions
themes = {
    'fruits': {
        3: {'fig': 'A small fruit with a sweet taste', 'pea': 'A small round green vegetable', 'nut': 'A hard-shelled fruit'},
        4: {'kiwi': 'A small brown fruit with green flesh', 'plum': 'A small purple fruit', 'pear': 'A green or yellow fruit'},
        5: {'apple': 'A round fruit with red or green skin', 'grape': 'A small round fruit used to make wine', 'mango': 'A tropical fruit with orange flesh'},
        6: {'banana': 'A long yellow fruit', 'orange': 'A round citrus fruit', 'tomato': 'A red fruit often used as a vegetable'}
    },
    'animals': {
        3: {'cat': 'A small domesticated carnivorous mammal', 'dog': 'A domesticated carnivorous mammal', 'bat': 'A nocturnal flying mammal'},
        4: {'lion': 'A large wild cat with a mane', 'wolf': 'A wild carnivorous mammal', 'bear': 'A large heavy mammal with thick fur'},
        5: {'zebra': 'An African wild horse with black-and-white stripes', 'tiger': 'A large wild cat with a striped coat', 'horse': 'A large domesticated mammal used for riding'},
        6: {'monkey': 'A small to medium-sized primate', 'giraffe': 'A tall African mammal with a long neck', 'rabbit': 'A small burrowing mammal with long ears'}
    },
    'colors': {
        3: {'red': 'The color of blood', 'tan': 'A light brown color', 'sky': 'The color of the sky on a clear day'},
        4: {'blue': 'The color of the ocean', 'pink': 'A pale red color', 'gold': 'A yellow precious metal'},
        5: {'green': 'The color of grass', 'white': 'The color of snow', 'black': 'The color of coal'},
        6: {'yellow': 'The color of the sun', 'orange': 'A color between red and yellow', 'purple': 'A color between red and blue'}
    }
}

# Create a 'none' key that combines other sublists of each length
themes['none'] = {
    length: {word: desc for theme in themes.values() for word, desc in theme[length].items()}
    for length in range(3, 7)
}

def word_picker(words):
    word, description = random.choice(list(words.items()))
    return word, description

def display_hangman(incorrect_guesses):
    stages = [
        """
           -----
           |   |
               |
               |
               |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        --------
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        --------
        """
    ]
    return stages[incorrect_guesses]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.user_data = self.load_user_data()
        self.username = None
        self.theme = None
        self.word_length = None
        self.word_to_guess = None
        self.word_description = None
        self.word_completion = None
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.max_incorrect_guesses = 6
        self.score = 0
        self.hints = 3
        self.words_guessed = 0
        self.total_games = 0
        self.highest_score = 0
        self.total_score = 0
        self.total_words_guessed = 0

        self.setup_gui()
        
    def load_user_data(self):
        if os.path.exists('user_data.json'):
            with open('user_data.json', 'r') as file:
                return json.load(file)
        return {}

    def save_user_data(self):
        with open('user_data.json', 'w') as file:
            json.dump(self.user_data, file, indent=4)

    def setup_gui(self):
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.username_var = tk.StringVar()
        self.username_label = tk.Label(self.scrollable_frame, text="Enter your username (leave blank for anonymous):")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.scrollable_frame, textvariable=self.username_var)
        self.username_entry.pack()
        self.submit_button = tk.Button(self.scrollable_frame, text="Submit", command=self.submit_username)
        self.submit_button.pack()
        self.signed_in_label = tk.Label(self.scrollable_frame, text="Not signed in.", font=("Courier", 12))
        self.signed_in_label.pack()

        self.sign_in_button = tk.Button(self.scrollable_frame, text="Sign In", command=self.show_login_screen)
        self.sign_in_button.pack_forget()

        self.sign_out_button = tk.Button(self.scrollable_frame, text="Sign Out", command=self.sign_out)
        self.sign_out_button.pack_forget()

        self.theme_var = tk.StringVar(value="Select a theme")
        self.length_var = tk.StringVar(value="Select word length")
        self.guess_var = tk.StringVar()

        self.theme_label = tk.Label(self.scrollable_frame, text="Select a theme:")
        self.theme_menu = tk.OptionMenu(self.scrollable_frame, self.theme_var, *themes.keys())

        self.length_label = tk.Label(self.scrollable_frame, text="Select word length:")
        self.length_menu = tk.OptionMenu(self.scrollable_frame, self.length_var, 3, 4, 5, 6)

        self.start_button = tk.Button(self.scrollable_frame, text="Start Game", command=self.start_game)

        self.stats_label = tk.Label(self.scrollable_frame, text="", font=("Courier", 12))

        self.alphabet_label = tk.Label(self.scrollable_frame, text="ABCDEFGHIJKLMNOPQRSTUVWXYZ", font=("Courier", 18))
        self.alphabet_label.pack_forget()

        self.hangman_label = tk.Label(self.scrollable_frame, text="", font=("Courier", 18))
        self.hangman_label.pack_forget()

        self.word_label = tk.Label(self.scrollable_frame, text="", font=("Courier", 18))
        self.word_label.pack_forget()

        self.description_label = tk.Label(self.scrollable_frame, text="", font=("Courier", 12))
        self.description_label.pack_forget()

        self.score_label = tk.Label(self.scrollable_frame, text="Score: 0", font=("Courier", 18))
        self.score_label.pack_forget()

        self.words_guessed_label = tk.Label(self.scrollable_frame, text="Words Guessed: 0", font=("Courier", 18))
        self.words_guessed_label.pack_forget()

        self.hints_label = tk.Label(self.scrollable_frame, text="Hints Available: 3", font=("Courier", 18))
        self.hints_label.pack_forget()

        self.wrong_guesses_label = tk.Label(self.scrollable_frame, text="Wrong Guesses Left: 6", font=("Courier", 18))
        self.wrong_guesses_label.pack_forget()

        self.guess_label = tk.Label(self.scrollable_frame, text="Enter your guess:")
        self.guess_label.pack_forget()

        self.guess_entry = tk.Entry(self.scrollable_frame, textvariable=self.guess_var)
        self.guess_entry.pack_forget()

        self.guess_button = tk.Button(self.scrollable_frame, text="Guess", command=self.guess_letter)
        self.guess_button.pack_forget()

        self.hint_button = tk.Button(self.scrollable_frame, text="Use Hint", command=self.use_hint)
        self.hint_button.pack_forget()

        self.profile_button = tk.Button(self.scrollable_frame, text="View Profile", command=self.view_profile)
        self.profile_button.pack_forget()

        self.all_profiles_button = tk.Button(self.scrollable_frame, text="View All Profiles", command=self.view_all_profiles)
        self.all_profiles_button.pack_forget()

    def submit_username(self):
        self.username = self.username_var.get().strip()
        if self.username == "":
            self.username = "Anonymous"
            messagebox.showinfo("Welcome", "You are playing as Anonymous. Your progress will not be saved.")
            self.sign_in_button.pack()
        else:
            if self.username in self.user_data:
                messagebox.showinfo("Welcome Back", f"Welcome back, {self.username}!")
                self.load_user_stats()
            else:
                messagebox.showinfo("Creating Account", f"Creating account for {self.username}.")
                self.user_data[self.username] = {
                    'total_games': 0,
                    'highest_score': 0,
                    'total_score': 0,
                    'total_words_guessed': 0
                }
                self.save_user_data()
            self.load_user_stats()

        self.signed_in_label.config(text=f"Signed in as: {self.username}")
        self.username_label.pack_forget()
        self.username_entry.pack_forget()  # Hide the username entry
        self.submit_button.pack_forget()  # Hide the submit button
        self.theme_label.pack()
        self.theme_menu.pack()
        self.length_label.pack()
        self.length_menu.pack()
        self.start_button.pack()
        self.profile_button.pack()
        self.all_profiles_button.pack()
        self.sign_out_button.pack()
    
    def sign_out(self):
        self.username = None
        self.signed_in_label.config(text="Signed out successfully.")
        self.username_label.pack()
        self.username_entry.pack()
        self.submit_button.pack()
        self.theme_label.pack_forget()
        self.theme_menu.pack_forget()
        self.length_label.pack_forget()
        self.length_menu.pack_forget()
        self.start_button.pack_forget()
        self.profile_button.pack_forget()
        self.all_profiles_button.pack_forget()
        self.sign_out_button.pack_forget()
        self.sign_in_button.pack_forget()
        self.hangman_label.pack_forget()
        self.word_label.pack_forget()
        self.description_label.pack_forget()
        self.score_label.pack_forget()
        self.words_guessed_label.pack_forget()
        self.hints_label.pack_forget()
        self.wrong_guesses_label.pack_forget()
        self.guess_label.pack_forget()
        self.guess_entry.pack_forget()
        self.guess_button.pack_forget()
        self.hint_button.pack_forget()

    def show_login_screen(self):
        self.username_entry.pack()
        self.submit_button.pack()
        self.sign_in_button.pack_forget()

    def load_user_stats(self):
        if self.username != "Anonymous":
            user_stats = self.user_data[self.username]
            self.total_games = user_stats['total_games']
            self.highest_score = user_stats['highest_score']
            self.total_score = user_stats['total_score']
            self.total_words_guessed = user_stats['total_words_guessed']
            self.update_stats_display()

    def save_user_stats(self):
        if self.username != "Anonymous":
            self.user_data[self.username] = {
                'total_games': self.total_games,
                'highest_score': self.highest_score,
                'total_score': self.total_score,
                'total_words_guessed': self.total_words_guessed
            }
            self.save_user_data()

    def start_game(self):
        self.theme = self.theme_var.get()
        self.word_length = int(self.length_var.get())
        if self.theme == "Select a theme":
            self.theme = 'none'
        word_list = themes[self.theme][self.word_length]
        self.word_to_guess, self.word_description = word_picker(word_list)
        self.word_completion = ['_'] * self.word_length
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.update_display()

        # Show the hidden labels and entry
        self.alphabet_label.pack()
        self.hangman_label.pack()
        self.word_label.pack()
        self.description_label.pack_forget()
        self.score_label.pack()
        self.words_guessed_label.pack()
        self.hints_label.pack()
        self.wrong_guesses_label.pack()
        self.guess_label.pack()
        self.guess_entry.pack()
        self.guess_button.pack()
        self.hint_button.pack()

        # Hide the start button and profile buttons
        self.start_button.pack_forget()
        self.profile_button.pack_forget()
        self.all_profiles_button.pack_forget()

    def end_round(self):
        # Hide the guess and hint areas
        self.hangman_label.pack_forget()
        self.word_label.pack_forget()
        self.description_label.pack_forget()
        self.score_label.pack_forget()
        self.words_guessed_label.pack_forget()
        self.hints_label.pack_forget()
        self.wrong_guesses_label.pack_forget()
        self.guess_label.pack_forget()
        self.guess_entry.pack_forget()
        self.guess_button.pack_forget()
        self.hint_button.pack_forget()

        # Show the final stats
        self.display_final_stats()

    def display_final_stats(self):
        # Hide game elements
        self.hangman_label.pack_forget()
        self.word_label.pack_forget()
        self.description_label.pack_forget()
        self.score_label.pack_forget()
        self.words_guessed_label.pack_forget()
        self.hints_label.pack_forget()
        self.wrong_guesses_label.pack_forget()
        self.guess_label.pack_forget()
        self.guess_entry.pack_forget()
        self.guess_button.pack_forget()
        self.hint_button.pack_forget()

        # Display final stats
        final_stats_text = (
            f"Final Score: {self.score}\n"
            f"Total Words Guessed: {self.words_guessed}\n"
            f"Total Games Played: {self.total_games}\n"
            f"Highest Score: {self.highest_score}\n"
        )
        self.final_stats_label = tk.Label(self.scrollable_frame, text=final_stats_text, font=("Courier", 12))
        self.final_stats_label.pack()

        # Display return button
        self.return_button = tk.Button(self.scrollable_frame, text="Return to Main Menu", command=self.return_to_main_menu)
        self.return_button.pack()

    def return_to_main_menu(self):
        # Hide final stats and return button
        self.final_stats_label.pack_forget()
        self.return_button.pack_forget()

        # Show main menu elements
        self.theme_label.pack()
        self.theme_menu.pack()
        self.length_label.pack()
        self.length_menu.pack()
        self.start_button.pack()
        self.profile_button.pack()
        self.all_profiles_button.pack()
        self.sign_out_button.pack()

    def update_display(self):
        self.hangman_label.config(text=display_hangman(self.incorrect_guesses))
        self.word_label.config(text=' '.join(self.word_completion))
        self.description_label.config(text=f"Hint: {self.word_description}")
        self.score_label.config(text=f"Score: {self.score}")
        self.words_guessed_label.config(text=f"Words Guessed: {self.words_guessed}")
        self.hints_label.config(text=f"Hints Available: {self.hints}")
        self.wrong_guesses_label.config(text=f"Wrong Guesses Left: {self.max_incorrect_guesses - self.incorrect_guesses}")
        self.update_alphabet_display()

    def update_alphabet_display(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        displayed_alphabet = ""
        for letter in alphabet:
            if letter.lower() in self.guessed_letters:
                displayed_alphabet += f"̶{letter}̶ "  # Strikethrough the guessed letter
            else:
                displayed_alphabet += f"{letter} "
        self.alphabet_label.config(text=displayed_alphabet)

    def update_stats_display(self):
        average_score = self.total_score / self.total_games if self.total_games > 0 else 0
        average_words_guessed = self.total_words_guessed / self.total_games if self.total_games > 0 else 0
        stats_text = (
            f"Total Games: {self.total_games}\n"
            f"Highest Score: {self.highest_score}\n"
            f"Average Score: {average_score:.2f}\n"
            f"Average Words Guessed: {average_words_guessed:.2f}"
        )
        self.stats_label.config(text=stats_text)

    def guess_letter(self):
        guess = self.guess_var.get().lower()
        self.guess_var.set("")

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Error", "Please enter a single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Info", "You have already guessed that letter. Try again.")
            return

        self.guessed_letters.add(guess)

        if guess in self.word_to_guess.lower():
            for i, letter in enumerate(self.word_to_guess.lower()):
                if letter == guess:
                    self.word_completion[i] = self.word_to_guess[i]  # Use the original case of the letter in the word
            if '_' not in self.word_completion:
                self.score += 2 - min(0, self.incorrect_guesses - 3)
                self.words_guessed += 1
                self.incorrect_guesses = max(0, self.incorrect_guesses - 3)  # Decrease incorrect guesses by 3 or set to 0
                
                messagebox.showinfo("Congratulations!", f"You guessed the word: {''.join(self.word_completion)}")
                self.hints += 1
                self.start_game()
        else:
            self.incorrect_guesses += 1
            if self.incorrect_guesses == self.max_incorrect_guesses:
                messagebox.showinfo("Game Over", f"Sorry, you ran out of guesses. The word was: {self.word_to_guess}")
                self.score += self.hints
                self.total_games += 1
                self.total_score += self.score
                self.total_words_guessed += self.words_guessed
                if self.score > self.highest_score:
                    self.highest_score = self.score
                self.update_stats_display()
                self.save_user_stats()
                self.end_round()

        self.update_display()

    def use_hint(self):
        if self.hints > 0:
            self.hints -= 1  # Decrease hints by 1 when a hint is used
            messagebox.showinfo("Hint", f"Hint: {self.word_description}")
        else:
            messagebox.showinfo("No hints available.")
        self.update_display()

    def view_profile(self):
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"{self.username}'s Profile")
        profile_stats = tk.Label(profile_window, text=self.stats_label.cget("text"), font=("Courier", 12))
        profile_stats.pack()

    def view_all_profiles(self):
        all_profiles_window = tk.Toplevel(self.root)
        all_profiles_window.title("All Profiles")
        all_profiles_text = ""
        for user, stats in self.user_data.items():
            average_score = stats['total_score'] / stats['total_games'] if stats['total_games'] > 0 else 0
            average_words_guessed = stats['total_words_guessed'] / stats['total_games'] if stats['total_games'] > 0 else 0
            all_profiles_text += (
                f"Username: {user}\n"
                f"Total Games: {stats['total_games']}\n"
                f"Highest Score: {stats['highest_score']}\n"
                f"Average Score: {average_score:.2f}\n"
                f"Average Words Guessed: {average_words_guessed:.2f}\n\n"
            )
        all_profiles_label = tk.Label(all_profiles_window, text=all_profiles_text, font=("Courier", 12))
        all_profiles_label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()