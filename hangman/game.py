from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guess, hit=False, miss=False):
        if hit is miss:
            raise InvalidGuessAttempt
        self.guess = guess
        self.hit = hit
        self.miss = miss

    def is_hit(self):
        return self.hit

    def is_miss(self):
        return self.miss


class GuessWord(object):
    def __init__(self, answer):
        if not answer:
            raise InvalidWordException

        self.answer = answer
        self.masked = '*' * len(answer)

    def perform_attempt(self, character):
        if not character or len(character) != 1:
            raise InvalidGuessedLetterException

        hit = False
        masked_list = list(self.masked)
        for index, char in enumerate(self.answer):
            if character.lower() == char.lower():
                masked_list[index] = character.lower()
                hit = True
        self.masked = ''.join(masked_list)

        if hit:
            return GuessAttempt(character, hit=True)
        return GuessAttempt(character, miss=True)


class HangmanGame(object):

    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, words=None, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        if words:
            self.words = words
        else:
            self.words = HangmanGame.WORD_LIST

        self.word = GuessWord(HangmanGame.select_random_word(self.words))
        self.previous_guesses = []

    def select_random_word(list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException
        return random.choice(list_of_words)

    def guess(self, character):
        if self.is_won() or self.is_lost():
            raise GameFinishedException

        attempt = self.word.perform_attempt(character)

        self.previous_guesses.append(character.lower())

        if attempt.is_miss():
            self.remaining_misses -= 1

        if self.is_lost():
            raise GameLostException

        if self.word.answer == self.word.masked:
            raise GameWonException

        return attempt

    def is_finished(self):
        return self.is_won() or self.is_lost()

    def is_lost(self):
        return self.remaining_misses < 1

    def is_won(self):
        return self.word.answer == self.word.masked
