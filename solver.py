import itertools
import random
import networkx as nx

# 10k source: https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt
# 25k source: https://github.com/gautesolheim/25000-syllabified-words-list/blob/master/25K-syllabified-sorted-alphabetically.txt

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
        ### POTENTIAL FUTURE DEVELOPMENT ###
        # An option for solving with hardest/most uncommon letters first
        # Use a hard-coded dict of letter frequency and bias selection of words
        # towards the least common letters first - that would prevent starting
        # with long words that use up 90% of the letters and then using a bunch
        # of junk/short words that reuse letters just to access the last letter
        # that needs to be hit
        # example: box is vhw/tdr/oje/auc
        # fast solution gives watchtower/revered/dutch/hot/taj
        # watchtower comes first because it uses the most letters but
        # you have to reuse a bunch of letters to get to taj at the end
        # because j is so rare
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
            
            # In theory you might need to add a step where you take a word that's
            # been added to the solution set out of the list of filtered words so
            # you don't repeat words in a solution. H O W E V E R . . . a word
            # you've already used will score a "0" on the "how many new letters
            # does this word provide" scale, so it should never be chosen as a
            # subsequent word

            if len(self.letters_used) == len(self.str_set):
                print("SOLUTION: ", self.fast_solution)
                break
            
            elif len(self.fast_solution) == self.max_words:
                self.solve_fast()
            
            else:
                continue

        return self.fast_solution
    
    # def solve_full(self):
    #     """
    #     (how="full") - brute-force listing of all possible winning moves
    #     """
    #     # Make dictionary of all available words and subsequent words they can link to
    #     word_links = {w1: list(filter(lambda w2: w2[0] == w1[-1] and w2 != w1, self.filt_words)) for w1 in self.filt_words}

    #     # For each word in the word_links dict, create all possible paths that:
    #     # 1. use all letters in the required set
    #     # 2. don't exceed the max number of allowable words
    #     # have to build this iteratively so that we're not using more words than necessary in any given solution
    #     DG = nx.DiGraph()
    #     node_list = list(word_links.keys())
    #     edge_list = []
    #     for k in word_links.keys():
    #         for v in word_links[k]:
    #             edge_list.append((k,v))
        
    #     DG.add_nodes_from(node_list)
    #     DG.add_edges_from(edge_list)

    #     solution_set = []
    #     for s in DG.nodes:
    #         for t in DG.nodes:
    #             for path in nx.all_simple_paths(DG, source=s, target=t):
    #                 if len(path) <= self.max_words and len(self.str_set) == len(''.join(path)):
    #                     solution_set.append(path)
    #                 else:
    #                     continue
            
    def solve(self, how="fast"):
        """
        """
        if how=="fast":
            self.solve_fast()
        else:
            pass
