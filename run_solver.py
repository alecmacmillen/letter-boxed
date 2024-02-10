import argparse
import nltk
from solver import Solver

parser = argparse.ArgumentParser()
parser.add_argument("--side1", type=str)
parser.add_argument("--side2", type=str)
parser.add_argument("--side3", type=str)
parser.add_argument("--side4", type=str)
parser.add_argument("--max_words", type=int, default=5)
parser.add_argument("--corpus", type=str, default=None)
parser.add_argument("--how", type=str, default="fast")

if __name__=="__main__":
    args = parser.parse_args()
    box = [args.side1, args.side2, args.side3, args.side4]

    solver = Solver(box=box, max_words=args.max_words, corpus=args.corpus)
    solver.solve(how=args.how)