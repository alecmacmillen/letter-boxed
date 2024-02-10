import itertools
import random

class Solver(object):
    def __init__(self, box, max_words, corpus=None):
        """
        Inputs:
            box (list): list of four 3-character lists,
                representing each side of the box
            max_words (int): max number of words allowed
            corpus (str): filepath to corpus of words used
                to solve, if none, will use 10k list
        """
        # Inputs from the daily game
        self.box = box
        self.max_words = max_words

        # Solver corpus inputs
        self.words = None
        if corpus is None:
            with open("25k.txt") as f:
                words = f.read().splitlines()
            self.words = [w.lower().replace(';','') for w in words]
        else:
            with open(corpus) as f:
                self.words = f.read().splitlines()
        
        self.accept = ''.join(self.box)
        self.str_set = set(self.accept)
        self.forbidden = self.find_forbidden()
        self.filt_words = self.filter_words(self.forbidden)

    def find_forbidden(self):
        """
        """
        forbidden = []
        for s in self.box:
            forbidden.extend(list(''.join(x) for x in itertools.permutations(s,2)))
            forbidden.extend(list(''.join(x)*2 for x in itertools.permutations(s, 1)))
        return forbidden
    
    def filter_words(self, forbidden):
        """
        """
        filt_words = list(
            filter(
                lambda w: set(w).issubset(self.accept) and
                    len(w)>=3 and
                    not any(f in w for f in forbidden),
                self.words
            )
        )
        return filt_words

    def solve_fast(self):
        """
        """
        self.fast_solution = []
        self.letters_used = set()
        self.letters_remaining = self.str_set - self.letters_used
        self.next_word_starts_with = None
        while len(self.fast_solution) < self.max_words and self.letters_used != self.str_set:
            # Find the words with the most unused letters
            # If the next word has to start with a certain letter, limit to only those words
            if self.next_word_starts_with is not None:
                available_words = list(filter(lambda w: w[0]==self.next_word_starts_with, self.filt_words))
                unique_chars = {w:len(set(w)&set(self.letters_remaining)) for w in available_words}
            # If not, just use any word with the max # of unused characters
            else:
                unique_chars = {w:len(set(w)&set(self.letters_remaining)) for w in self.filt_words}
           
            # List of next-word options that have the most number of unused characters
            word_options = list(dict(filter(lambda p: p[1]==max(unique_chars.values()), unique_chars.items())).keys())
            try:
                word = random.choice(word_options)
            except IndexError:
                print("Word options list is empty. Exiting solver")
                break

            # Add the selected word to the solution list and update the set of 
            # letters used and remaining, and find the letter the next starts with
            self.fast_solution.append(word)
            self.letters_used.update(set(word))
            self.letters_remaining = self.str_set - self.letters_used
            self.next_word_starts_with = word[-1]

            if len(self.letters_used) == len(self.str_set):
                print("SOLUTION: ", self.fast_solution)
                break
            
            elif len(self.fast_solution) == self.max_words:
                self.solve_fast()
            
            else:
                continue

        return self.fast_solution
    
    def solve(self, how="fast"):
        """
        """
        if how=="fast":
            self.solve_fast()
        else:
            pass



# 10k source: https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt
# 25k source: https://github.com/gautesolheim/25000-syllabified-words-list/blob/master/25K-syllabified-sorted-alphabetically.txt

# (how="all") - brute-force listing of all possible winning moves

# (how="random") where a random word is picked, then another
# random word, and so on and so forth until either the solution condition
# is met or the number of words is maxed out, in which case another random
# word is selected and on we go