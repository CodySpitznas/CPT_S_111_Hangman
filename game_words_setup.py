'''
- Asher Wu, Cody Spitznas
- 12/9/24
- CptS 111, Fall 2024
- Hangman Marathon
- This project simulates the game of Hangman.
- Modules used: random, word_dictionaries
'''

import random
from word_dictionaries import *

# Define themes and their corresponding word lists with descriptions
themes = {
    'holidays':
    {
        3: holiday_words_3,
        4: holiday_words_4,
        5: holiday_words_5,
        6: holiday_words_6,
        7: holiday_words_7,
        8: holiday_words_8,
        9: holiday_words_9,
        10: holiday_words_10
    },
    'animals':
    {
        3: animal_words_3,
        4: animal_words_4,
        5: animal_words_5,
        6: animal_words_6,
        7: animal_words_7,
        8: animal_words_8,
        9: animal_words_9,
        10: animal_words_10
    },
    'geography':
    {
        3: geography_words_3,
        4: geography_words_4,
        5: geography_words_5,
        6: geography_words_6,
        7: geography_words_7,
        8: geography_words_8,
        9: geography_words_9,
        10: geography_words_10
    },
    'fantasy':
    {
        3: fantasy_words_3,
        4: fantasy_words_4,
        5: fantasy_words_5,
        6: fantasy_words_6,
        7: fantasy_words_7,
        8: fantasy_words_8,
        9: fantasy_words_9,
        10: fantasy_words_10
    },
    'history':
    {
        3: history_words_3,
        4: history_words_4,
        5: history_words_5,
        6: history_words_6,
        7: history_words_7,
        8: history_words_8,
        9: history_words_9,
        10: history_words_10
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
