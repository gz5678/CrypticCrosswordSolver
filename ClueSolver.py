import itertools
import math
import GrammarDefinitions
import nltk
import os.path
import SimilaritySolver

ANAG_MAX = 9
MIN_SOLUTION_VALUE = 0


def solve(clue, solution_format):
    # Define parser
    grammar_str = GrammarDefinitions.define_grammar(clue)
    grammar = nltk.CFG.fromstring(grammar_str)
    parser = nltk.ChartParser(grammar)

    solutions = []

    # Get all possible solutions
    for tree in parser.parse(clue):
        type = tree[0].label()
        solutions += SOLVER_DICT[type](tree[0], solution_format)

    # Filter only relevant solutions
    solutions.sort(key=lambda x: x[1], reverse=True)
    solutions = [solution for solution in solutions if solution[1] > MIN_SOLUTION_VALUE and solution[0] not in clue]

    return solutions


def _solve_double_synonym(parse_tree, solution_format=None):
    return []
    # def _get_value(solution_list, word):
    #     for solution in solution_list:
    #         if solution[0] == word:
    #             return solution[1]
    #
    #     return 0
    #
    # first_syn, second_syn = _get_parts_ignore_EQU(parse_tree)
    #
    # if solution_format is not None:
    #     first_solutions = SimilaritySolver.solve(first_syn, length=solution_format.get_total_length(spaces=True))
    #     second_solutions = SimilaritySolver.solve(second_syn, length=solution_format.get_total_length(spaces=True))
    #     second_words = [word for word, _ in second_solutions if solution_format.check(word)]
    # else:
    #     first_solutions = SimilaritySolver.solve(first_syn)
    #     second_solutions = SimilaritySolver.solve(second_syn)
    #     second_words = [word for word, _ in second_solutions]
    #
    # solutions = [solution for solution in first_solutions if solution[0] in second_words]
    # for solution in solutions:
    #     solution[1] = math.sqrt(_get_value(second_solutions, solution[0]) * solution[1])
    #
    # return solutions


def _solve_anagram(parse_tree, solution_format=None):
    anag, syn = _get_parts_ignore_EQU(parse_tree)

    anag_word = anag[0]
    if not anag_word.label() == 'ANAG_WORD':
        anag_word = anag[1]
    anag_word = _create_sentence(anag_word, space=False)

    syn_sent = _create_sentence(syn)
    if len(anag_word) > ANAG_MAX:
        return []
    words = ["".join(perm) for perm in itertools.permutations(anag_word)]
    if solution_format is not None:
        words = [solution_format.add_spaces(word) for word in words if solution_format.check(word)]

    solutions = [(word, SimilaritySolver.solve(syn_sent, 0, word.replace(" ", "_"))) for word in words]

    return solutions


def _solve_reverse(parse_tree, solution_format=None):
    _handle_abbreviations(parse_tree)
    reverse, syn = _get_parts_ignore_EQU(parse_tree)

    reverse_word = reverse[0]
    if not reverse_word.label() == 'REV_WORD':
        reverse_word = reverse[1]

    reverse_word = _create_sentence(reverse_word, space=False, abbr=True)
    reversed = reverse_word[::-1]  # reverse word
    if solution_format is not None:
        if not solution_format.check(reversed):
            return []
        reversed = solution_format.add_spaces(reversed)

    syn_sent = _create_sentence(syn)
    return [(reversed, SimilaritySolver.solve(syn_sent, 0, reversed.replace(" ", "_")))]


def _solve_enclosure(parse_tree, solution_format=None):
    _handle_abbreviations(parse_tree)
    enclose, syn = _get_parts_ignore_EQU(parse_tree)

    enc_word = enclose[0]
    ins_word = enclose[2]
    enc_word = _create_sentence(enc_word, space=False, abbr=True)
    ins_word = _create_sentence(ins_word, space=False, abbr=True)

    syn_sent = _create_sentence(syn)

    return _get_all_insertions(syn_sent, enc_word, ins_word, solution_format)


def _solve_insertion(parse_tree, solution_format=None):
    _handle_abbreviations(parse_tree)
    insert, syn = _get_parts_ignore_EQU(parse_tree)

    ins_word = insert[0]
    enc_word = insert[2]
    ins_word = _create_sentence(ins_word, space=False, abbr=True)
    enc_word = _create_sentence(enc_word, space=False, abbr=True)

    syn_sent = _create_sentence(syn)

    return _get_all_insertions(syn_sent, enc_word, ins_word, solution_format)


def _get_all_insertions(synonym, enc_word, ins_word, solution_format=None):
    words = [enc_word[0:i] + ins_word + enc_word[i:] for i in range(1, len(enc_word))]
    if solution_format is not None:
        words = [solution_format.add_spaces(word) for word in words if solution_format.check(word)]

    solutions = [(word, SimilaritySolver.solve(synonym, 0, word.replace(" ", "_"))) for word in words]
    return solutions


def _solve_hidden_word(parse_tree, solution_format=None):
    hidden, syn = _get_parts_ignore_EQU(parse_tree)

    hiding_word = hidden[0]
    if not hiding_word.label() == 'HID_WORD':
        hiding_word = hidden[1]

    hiding_word = _create_sentence(hiding_word, space=False)

    syn_sent = _create_sentence(syn)

    if solution_format is not None:
        total_length = solution_format.get_total_length()
        words = [hiding_word[i:i + total_length] for i in range(len(hiding_word) - total_length + 1)]
        words = [word for word in words if solution_format.check(word)]
    else:
        words = []
        for length in range(1, len(hiding_word)):
            words += [hiding_word[i:i + length] for i in range(len(hiding_word) - length + 1)]

    solutions = [(word, SimilaritySolver.solve(syn_sent, 0, word.replace(" ", "_"))) for word in words]

    return solutions


def _get_parts_ignore_EQU(parse_tree):
    first_part = parse_tree[0]
    second_part = parse_tree[1]
    if second_part.label() == 'EQU':
        second_part = parse_tree[2]

    if first_part.label() == 'SYN':
        syn = first_part
        other = second_part
    else:
        syn = second_part
        other = first_part

    return other, syn


def _create_sentence(parse_tree, space=True, abbr=False):
    word = parse_tree[0][0]
    if abbr:
        word = word[0]
    if len(parse_tree) == 1:
        return word
    else:
        if space:
            return word + " " + _create_sentence(parse_tree[1], space=space, abbr=abbr)
        else:
            return word + _create_sentence(parse_tree[1], space=False, abbr=abbr)


def _handle_abbreviations(parse_tree):
    path = os.path.join(GrammarDefinitions.FOLDER, GrammarDefinitions.ABBREVIATION_FILE)
    with open(path, "r") as f:
        lines = f.read().splitlines()

    abbr_dict = {line.split(GrammarDefinitions.ABBR_SEP)[0]: line.split(GrammarDefinitions.ABBR_SEP)[1] for line in
                 lines}
    _replace_abbreviation(parse_tree, abbr_dict)


def _replace_abbreviation(parse_tree, abbr_dict):
    if not isinstance(parse_tree, nltk.Tree):
        return

    if parse_tree.label() == 'ABBR':
        word = parse_tree[0]
        parse_tree.set_label('WORD')
        parse_tree[0] = abbr_dict[word]
        return

    for son in parse_tree:
        _replace_abbreviation(son, abbr_dict)


SOLVER_DICT = {"DOUBLE_SYN": _solve_double_synonym,
               "ANAG": _solve_anagram,
               "REVERSE": _solve_reverse,
               "ENCLOSE": _solve_enclosure,
               "INSERT": _solve_insertion,
               "HIDDEN": _solve_hidden_word
               }
