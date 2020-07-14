import string
from SolutionFormat import SolutionFormat
from ClueSolver import solve


def CrypticSolver():
    print_header()
    run = True

    while run:
        # Get the clue, strip punctuation and change to lower case
        clue_str = input("Insert the clue:\n").translate(str.maketrans('', '', string.punctuation))
        clue = [word.lower() for word in clue_str.split(" ")]

        length_str = input("Insert the number of letters in the solution:\n")
        if length_str == "":
            solution_format = None
        else:
            try:
                # Get lengths of words
                split = length_str.split(",")
                lengths = [int(length) for length in split]
            except ValueError:
                print("Illegal input. Format will be ignored when trying to solve the clue.")
                lengths = []

            if len(lengths) > 0:
                format_str = input("Insert the known letters in the solution.\n")
                try:
                    # Get known letters
                    solution_format = SolutionFormat(len(lengths), lengths, format_str)
                except ValueError:
                    print("Illegal input. Format will be ignored when trying to solve the clue.")
                    solution_format = None
            else:
                solution_format = None

        solutions = solve(clue, solution_format)
        print_solutions(solutions)

        run = print_end()


def print_header():
    print("Welcome to our Cryptic Clue Solver 1.0.\n"
          "This program allows you to get help with your cryptic crossword, with others being judgemental of your abilities.\n"
          "----------------------------------------------------------------------------------------------\n"
          "Guide for the program:\n"
          "The first part is simple, just enter your clue and press enter.\n"
          "Then you would need to insert anything you know about the solution. First, insert the number of letters in the solution.\n"
          "If the solution has multiple words, simply enter their lengths by order, separated by a comma (,).\n"
          "If you don't know the number of letters, don't worry, we still have you covered. Just press enter and our program will try to solve the clue anyway.\n"
          "If you have entered the number of letters, not you can enter the letters you already know.\n"
          "Simply write down the entire solution, with an underscore (_) replacing any letter you don't know.\n"
          "Make sure to add spaces between words and to add the right number of letters and underscores.\n"
          "If you don't know any letter, you can simply press enter.\n"
          "Okay, we are done with the explanations. You can now start trying out our program. Press enter to start.")
    input()
    print("----------------------------------------------------------------------------------------------")


def print_end():
    i = input("To quit insert 'quit'. To continue press enter.\n")
    if i == 'quit':
        print("Thank you for using our Cryptic Clue Solver 1.0!")
        return False
    else:
        print("----------------------------------------------------------------------------------------------")
        return True


def print_solutions(solutions):
    if len(solutions) == 0:
        print("No plausible solutions found.")
        return

    print("The best possible solution we found was '%s'" % solutions[0][0])
    print("Match score: %s" % solutions[0][1])
    if len(solutions) > 1:
        print("Other possible solutions include:")
        for word, score in solutions[1:]:
            print(word + " score: %s" % score)


CrypticSolver()
