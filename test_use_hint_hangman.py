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

class TestUseHintHangmanGame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.game = HangmanGame(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.messagebox.showinfo')
    def test_use_hint_with_hints_available(self, mock_showinfo):
        self.game.word_description = "A shrub or tree with prickly dark green leaves, small white flowers, and red berries."
        self.game.hints = 3
        self.game.word_completion = ['_', '_', '_', '_', '_']
        self.game.use_hint()
        self.assertEqual(self.game.hints, 2)
        mock_showinfo.assert_called_with("Hint", "Hint: A shrub or tree with prickly dark green leaves, small white flowers, and red berries.")

    @patch('tkinter.messagebox.showinfo')
    def test_use_hint_no_hints_available(self, mock_showinfo):
        self.game.word_description = "A shrub or tree with prickly dark green leaves, small white flowers, and red berries."
        self.game.hints = 0
        self.game.word_completion = ['_', '_', '_', '_', '_']
        self.game.use_hint()
        self.assertEqual(self.game.hints, 0)
        mock_showinfo.assert_called_with("No hints available.")

if __name__ == '__main__':
    unittest.main()