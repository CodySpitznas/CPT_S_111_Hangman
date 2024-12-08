import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from game import HangmanGame, themes

class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.game = HangmanGame(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.messagebox.showinfo')
    def test_submit_username_anonymous(self, mock_showinfo):
        self.game.username_var.set("")
        self.game.submit_username()
        self.assertEqual(self.game.username, "Anonymous")
        mock_showinfo.assert_called_with("Welcome", "You are playing as Anonymous. Your progress will not be saved.")

    @patch('tkinter.messagebox.showinfo')
    def test_submit_username_existing_user(self, mock_showinfo):
        self.game.user_data = {"testuser": {"total_games": 1, "highest_score": 10, "total_score": 10, "total_words_guessed": 5}}
        self.game.username_var.set("testuser")
        self.game.submit_username()
        self.assertEqual(self.game.username, "testuser")
        mock_showinfo.assert_called_with("Welcome Back", "Welcome back, testuser!")

    @patch('tkinter.messagebox.showinfo')
    def test_submit_username_new_user(self, mock_showinfo):
        self.game.user_data = {}
        self.game.username_var.set("newuser")
        self.game.submit_username()
        self.assertEqual(self.game.username, "newuser")
        mock_showinfo.assert_called_with("Creating Account", "Creating account for newuser.")
        self.assertIn("newuser", self.game.user_data)

    @patch('random.choice', return_value=("feast", "A large meal, typically one in celebration of something."))
    def test_start_game(self, mock_choice):
        self.game.theme_var.set("holidays")
        self.game.length_var.set("5")
        self.game.start_game()
        self.assertEqual(self.game.theme, "holidays")
        self.assertEqual(self.game.word_length, 5)
        self.assertEqual(self.game.word_to_guess, "feast")
        self.assertEqual(self.game.word_description, "A large meal, typically one in celebration of something.")
        self.assertEqual(self.game.word_completion, ['_', '_', '_', '_', '_'])
        self.assertEqual(self.game.incorrect_guesses, 0)

if __name__ == '__main__':
    unittest.main()