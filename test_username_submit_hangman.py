'''
- Asher Wu, Cody Spitznas
- 12/9/24
- CptS 111, Fall 2024
- Hangman Marathon
- This project simulates the game of Hangman.
- Modules used: unittest, tkinter, game
'''

import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from game import HangmanGame, themes

class TestUsernameSubmitHangmanGame(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()