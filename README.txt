CRYPTIC CLUE SOLVER 1.0

This project includes the implementation of the Cryptic Clue Solver 1.0 (CCS1) as well as additional required files.

FILE LIST

README.txt							this file
Code files
	ClueSolver.py					Given a single parse tree for a clue, finds as many solutions as possible
	CrypticSolver.py				Main script for inputting clues manually
	GrammarDefinitions.py			Creates the CFG rules
	SimilaritySolver.py				Calculates the similarity score of a given (regular) clue and different possible solutions
	SolutionFormat.py				Defines an object representing the format of a clue's solution (number of words and letters and known letters)
	SolverFromFile.py				Main script for solving several clues from a file
Clues
	ClueList.txt					A list of 146 clues
	ClueList_Results.txt			The output of the SolverFromFile script on the ClueList.txt file
Word lists
	ABBR.txt						List of common abbreviations (e.g. doctor -> doc)
	ANAG_IDT.txt					List of indicator words for anagram clues
	ENC_IDT.txt						List of indicator words for enclosure clues
	EQU.txt							List of words indication equality (these words are ignored when parsing the clue). The list contains only "is" and should be expanded in the future
	HID_IDT.txt						List of indicator words for hidden word clues
	INS_IDT.txt						List of indicator words for insertion clues
	REV_IDT.txt						List of indicator words for reversal clues
Submission files
	CFG Definition.txt				The complete Context-Free Grammar definition used by the program (the program creates the list dynamically rather than use this file)
	Project Article.pdf				The article written to sum up the project

REQUIREMENTS

1. Python 3
2. Python's Natural Language Toolkit (NLTK)
3. NLTK's complete data (using NLTK's data downloader)

RUNNING THE PROGRAM

The project has two runnable scripts: one for inputting clues manually and one for running complete lists of clues:
1. CrypticSolver
					Simply run the script with no parameters. Usage instructions will be printed out for the user.
2.SolverFromFile
					To run this script, the list of clues should be saved in a text file, where each line is a clue in the following format:
					#clue# (#num of letters#) | #solution#
					The file should be saved in the Clues folder, and the global variables INPUT_FILE_NAME and OUTPUT_FILE_NAME in the script should be updated.

