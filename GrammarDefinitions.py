"""
This file is used to define the entire Context-Free Grammar for solving cryptic clues. It combines rules for each type
of clue, general rules, rules for identifying possible abbreviations and possible indicator words.
Abbreviation and indicator words are pulled from text files.
The WORD rule is defined by the specific words in the clue (rather than having a general rule for all words).
"""


import os.path

IDENTIFIER_TYPES = ["ANAG_IDT", "REV_IDT", "ENC_IDT", "INS_IDT", "HID_IDT", "EQU"]
CLUE_TYPES = {
    "DOUBLE_SYN": """
                        DOUBLE_SYN -> SYN EQU SYN | SYN SYN
                    """,
    "ANAG": """
                        ANAG -> SYN EQU ANAG_SEN | SYN ANAG_SEN | ANAG_SEN EQU SYN | ANAG_SEN SYN
                        ANAG_SEN -> ANAG_IDT ANAG_WORD | ANAG_WORD ANAG_IDT
                        ANAG_WORD -> WORD ANAG_WORD | WORD
                    """,

    "REVERSE": """
                        REVERSE -> SYN EQU REV_SEN | SYN REV_SEN | REV_SEN EQU SYN | REV_SEN SYN
                        REV_SEN -> REV_IDT REV_WORD | REV_WORD REV_IDT
                        REV_WORD -> WORDABBR REV_WORD | WORDABBR
                    """,
    "ENCLOSE": """
                        ENCLOSE -> SYN EQU ENC_SEN | SYN ENC_SEN | ENC_SEN EQU SYN | ENC_SEN SYN
                        ENC_SEN -> ENC_WORD ENC_IDT INS_WORD
                        ENC_WORD -> WORDABBR ENC_WORD | WORDABBR
                        INS_WORD -> WORDABBR INS_WORD | WORDABBR
                    """,
    "INSERT": """
                        INSERT -> SYN EQU INS_SEN | SYN INS_SEN | INS_SEN EQU SYN | INS_SEN SYN
                        INS_SEN -> INS_WORD INS_IDT ENC_WORD
    """,              # ENC_WORD -> WORDABBR ENC_WORD | WORDABBR
                      # INS_WORD -> WORDABBR INS_WORD | WORDABBR
                      # Already defined for ENCLOSE. Add definitions if necessary.
    "HIDDEN": """
                        HIDDEN -> SYN EQU HID_SEN | SYN HID_SEN | HID_SEN EQU SYN | HID_SEN SYN
                        HID_SEN -> HID_IDT HID_WORD | HID_WORD HID_IDT
                        HID_WORD -> WORD HID_WORD | WORD
    """
}

GENERAL_RULES = ["SYN -> WORD SYN | WORD",
                 "WORDABBR -> WORD | ABBR"]

ABBREVIATION_FILE = "ABBR.txt"
ABBR_SEP = "---"
FOLDER = "Word lists"

def define_grammar(clue):
    initial_rule = "S -> " + " | ".join(CLUE_TYPES.keys())                  # S -> all clue types
    clue_types_rules = "\n".join(CLUE_TYPES.values())
    general_rules = "\n".join(GENERAL_RULES)
    word_rule = "WORD ->" + " | ".join(["'%s'" % word for word in clue])    # WORD -> all words in the clue
    identifiers_rule = create_identifiers_rules()
    abbreviation_rule = create_abbreviation_rule()
    grammar = initial_rule + "\n" + clue_types_rules + "\n" + general_rules + "\n" + identifiers_rule + \
              "\n" + abbreviation_rule + "\n" + word_rule
    return grammar


def create_identifiers_rules():
    rules = ""
    for type in IDENTIFIER_TYPES:
        rule = create_rule_from_file(type, type + ".txt")
        rules += (rule + "\n")

    return rules


def create_rule_from_file(rule_name, file_name):
    path = os.path.join(FOLDER, file_name)

    with open(path, "r") as f:
        words = f.read().splitlines()

    words = [word.lower() for word in words]
    rule = rule_name + " -> " + " | ".join(["'%s'" % word for word in words])  # IDENTIFIER TYPE -> all identifier words

    return rule


def create_abbreviation_rule():
    path = os.path.join(FOLDER, ABBREVIATION_FILE)
    with open(path, "r") as f:
        lines = f.read().splitlines()

    words = [line.split(ABBR_SEP)[0].lower() for line in lines]
    rule = "ABBR -> " + " | ".join(["'%s'" % word for word in words])   # ABBR -> all words that can be abbreviated

    return rule
