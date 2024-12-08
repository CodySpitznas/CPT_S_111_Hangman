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
from game import HangmanGame

class TestGuessLetterHangmanGame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.game = HangmanGame(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.messagebox.showinfo')
    def test_guess_letter_correct(self, mock_showinfo):
        self.game.word_to_guess = "holly"
        self.game.word_completion = ['_', '_', '_', '_', '_']
        self.game.guessed_letters = set()
        self.game.incorrect_guesses = 0
        self.game.guess_var.set("h")
        self.game.guess_letter()
        self.assertIn("h", self.game.guessed_letters)
        self.assertEqual(self.game.word_completion, ['h', '_', '_', '_', '_'])
        self.assertEqual(self.game.incorrect_guesses, 0)

    @patch('tkinter.messagebox.showinfo')
    def test_guess_letter_incorrect(self, mock_showinfo):
        self.game.word_to_guess = "holly"
        self.game.word_completion = ['_', '_', '_', '_', '_']
        self.game.guessed_letters = set()
        self.game.incorrect_guesses = 0
        self.game.guess_var.set("z")
        self.game.guess_letter()
        self.assertIn("z", self.game.guessed_letters)
        self.assertEqual(self.game.word_completion, ['_', '_', '_', '_', '_'])
        self.assertEqual(self.game.incorrect_guesses, 1)

    @patch('tkinter.messagebox.showinfo')
    def test_guess_letter_already_guessed(self, mock_showinfo):
        self.game.word_to_guess = "holly"
        self.game.word_completion = ['_', '_', '_', '_', '_']
        self.game.guessed_letters = {'h'}
        self.game.incorrect_guesses = 0
        self.game.guess_var.set("h")
        self.game.guess_letter()
        mock_showinfo.assert_called_with("Info", "You have already guessed that letter. Try again.")
        self.assertEqual(self.game.incorrect_guesses, 0)
if __name__ == '__main__':
    unittest.main()