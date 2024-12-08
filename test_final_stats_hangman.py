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

class TestFinalStatsHangmanGame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.game = HangmanGame(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.Label')
    @patch('tkinter.Button')
    def test_display_final_stats(self, mock_button, mock_label):
        # Set up the game state
        self.game.score = 10
        self.game.words_guessed = 5
        self.game.total_games = 3
        self.game.highest_score = 15

        # Call the function to display final stats
        self.game.display_final_stats()

        # Verify that the final stats label is created with the correct text
        final_stats_text = (
            f"Final Score: {self.game.score}\n"
            f"Total Words Guessed: {self.game.words_guessed}\n"
            f"Total Games Played: {self.game.total_games}\n"
            f"Highest Score: {self.game.highest_score}\n"
        )
        mock_label.assert_called_with(self.game.scrollable_frame, text=final_stats_text, font=("Courier", 12))
        mock_label.return_value.pack.assert_called_once()

        # Verify that the return button is created and packed
        mock_button.assert_called_with(self.game.scrollable_frame, text="Return to Main Menu", command=self.game.return_to_main_menu)
        mock_button.return_value.pack.assert_called_once()

if __name__ == '__main__':
    unittest.main()