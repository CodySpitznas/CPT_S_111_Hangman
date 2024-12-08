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

class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.game = HangmanGame(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('random.choice', return_value=("holly", "A shrub or tree with prickly dark green leaves, small white flowers, and red berries."))
    def test_start_game(self, mock_choice):
        self.game.theme_var.set("holidays")
        self.game.length_var.set("5")
        self.game.start_game()
        self.assertEqual(self.game.theme, "holidays")
        self.assertEqual(self.game.word_length, 5)
        self.assertEqual(self.game.word_to_guess, "holly")
        self.assertEqual(self.game.word_description, "A shrub or tree with prickly dark green leaves, small white flowers, and red berries.")
        self.assertEqual(self.game.word_completion, ['_', '_', '_', '_', '_'])
        self.assertEqual(self.game.incorrect_guesses, 0)

if __name__ == '__main__':
    unittest.main()