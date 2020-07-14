from ClueSolver import solve, MIN_SOLUTION_VALUE
from SolutionFormat import SolutionFormat
import string
import os.path
import time

FOLDER = "Clues"
INPUT_FILE_NAME = "DifferentClues3.txt"
OUTPUT_FILE_NAME = "DifferentClues3_Results.txt"

def SolveFromFile():
    print("Solving clues in file %s" % INPUT_FILE_NAME)
    clues = parse_file(os.path.join(FOLDER, INPUT_FILE_NAME))

    num_of_clues = len(clues)
    found = 0
    correct = 0
    was_option = 0

    path = os.path.join(FOLDER, OUTPUT_FILE_NAME)
    start = time.time()
    with open(path, "w", encoding="utf-8") as f:
        for clue, solution_format, solution in clues:
            solutions = solve(clue, solution_format)
            if solutions and solutions[0][1] > MIN_SOLUTION_VALUE:
                found += 1
                if solutions[0][0] == solution:
                    correct += 1
                    was_option += 1
                    f.write("%s. Correct solution found: %s\n" % (" ".join(clue), solutions[0][0]))
                else:
                    possibility = False
                    for word,score in solutions:
                        if solution == word:
                            f.write("%s. Correct solution (%s) got score %s.\n" % (" ".join(clue), word, score))
                            possibility = True
                            was_option += 1
                    if not possibility:
                        f.write("%s. Incorrect solution found: %s\n" % (" ".join(clue), solutions[0][0]))
            else:
                f.write("%s. No solution.\n" % " ".join(clue))
    total = time.time() - start

    print("Total number of clues: %s\n"
          "Solutions found: %s (%s %% of clues))\n"
          "Correct solutions found: %s (%s%% of clues, %s%% of solutions)\n"
          "The correct solution was one of the options %s times (%s%% of clues, %s%% of solutions)\n"
          "Calculation lasted %s seconds.\n"
          % (num_of_clues, found, 100 * found / num_of_clues, correct, 100 * correct / num_of_clues,
             100 * correct / found, was_option, 100 * was_option / num_of_clues, 100 * was_option / found, total))


def parse_file(path):
    with open(path, "r", encoding="utf-8") as f:
        all_clues = f.readlines()

    clues = [parse_line(line) for line in all_clues]
    return clues

def parse_line(line):
    first_bracket = line.rfind("(")
    second_bracket = line.rfind(")")
    separator = line.rfind("|")

    clue_str = line[:first_bracket - 1].translate(str.maketrans('', '', string.punctuation))
    clue = [word.lower().strip() for word in clue_str.split(" ")]
    clue = [word for word in clue if len(word) > 0]
    lengths_str = line[first_bracket + 1:second_bracket].split(",")
    lengths = [int(length) for length in lengths_str]
    solution = line[separator + 1:].lower().strip()

    return clue, SolutionFormat(len(lengths), lengths, ""), solution

SolveFromFile()