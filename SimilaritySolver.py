from nltk.corpus import wordnet as wn, stopwords
from nltk.tokenize import word_tokenize
import re


def solve(clue, length=0, solution = "", indicator=True):
    """
    Return a sorted list of words and their score that are possible solutions to the clue given.
    The length of word, when given, is used as a filtering factor.
    If a solution is given, the score of the solution as an answer to the clue is returned.
    :param clue: The clue we want to give solutions.
    :param length: The length of the solution.
    :param solution: A given solution to the clue
    :return: A list of words and their scores as solutions to the clue or, given a solution, it's score as a
    solution to the clue.
    """
    stop_words = set(stopwords.words("english"))
    text_words = word_tokenize(clue)  # tokenize the clue
    temp_words = list(set(text_words) - stop_words)  # remove functional words
    if len(temp_words) != 0:
        text_words = temp_words
    syn = []

    # create array of all synsets of the context words
    for i, val in enumerate(text_words):
        syn.extend(wn.synsets(val))

    syn_verb = []
    for i, val in enumerate(text_words):
        syn_verb.extend(wn.synsets(val, pos=wn.VERB))

    syn_noun = []
    for i, val in enumerate(text_words):
        syn_noun.extend(wn.synsets(val, pos=wn.NOUN))

    syn_adj = []
    for i, val in enumerate(text_words):
        syn_adj.extend(wn.synsets(val, pos=wn.ADJ))

    syn_adv = []
    for i, val in enumerate(text_words):
        syn_adv.extend(wn.synsets(val, pos=wn.ADV))

    # check if any synsets found
    if len(syn) == 0:
        return 0
    context_words = []

    # iterate over all the synsets of all the non functional words in the clue
    # tokenize the definitions and remove all the functional words
    for i, val in enumerate(syn):
        words = word_tokenize(val.definition())
        context_words.extend(words)

    # this is a list of all the context words of all the definitions of all the synsets
    # of all the context words in the clue
    #context_words = list(set(context_words) - stop_words)
    context_words = _remove_non_alphabet(context_words)

    iteration_list = []

    if solution:  # We only want to check one word similarity, which is given as an argument.
        iteration_list.append(solution)
    else:
        iteration_list = list(wn.all_lemma_names(lang='eng'))

    # iterate over all the values in the database
    output_noun, output_verb, output_adj, output_adv, output_lesk = _give_score(iteration_list, length, context_words, text_words, syn, syn_noun, syn_verb, syn_adj, syn_adv)
    lesk = sorted(output_lesk, key=output_lesk.__getitem__, reverse=True)

    tot_rank1 = {k: max(i for i in (output_verb.get(k), output_noun.get(k)) if i) for k in
                 output_verb.keys() | output_noun}

    tot_rank2 = {k: max(i for i in (tot_rank1.get(k), output_adj.get(k)) if i) for k in
                 tot_rank1.keys() | output_adj}

    tot_rank = {k: max(i for i in (tot_rank2.get(k), output_adv.get(k)) if i) for k in
                tot_rank2.keys() | output_adv}

    for w in lesk:
        # word only found in lesk
        if not (w in tot_rank) or tot_rank[w] == 0:
            tot_rank[w] = output_lesk[w]
        # word that got a similarity score of 1
        elif tot_rank[w] == 1:
            tot_rank[w] = 1
        else:
            tot_rank[w] = (output_lesk[w] + tot_rank[w])/2

    if solution:  # If we just want the score for the word as a solution to the clue.
        try:
            score = tot_rank[solution]
        except KeyError:
            score = 0
        if len(clue.split()) == 1 and indicator:
            symmetric_score = solve(solution, length, clue, False)
            return max(symmetric_score, score)
        else:
            return score
    rank = list(tot_rank.items())

    return sorted(rank, key=lambda x: x[1], reverse=True)[:1000]


def _remove_non_alphabet(word_list):
    """
    Removes all non words from the token list.
    :param word_list: A list of word tokens.
    :return: The same list without non-words.
    """
    update_word_list = []
    pattern = re.compile("/('?\w+)|(\w+'\w+)|(\w+'?)|(\w+)/")
    for word in word_list:
        if pattern.match(word):
            update_word_list.append(word)
    return update_word_list


def _give_score(word_list, length, context_words, clue_tokens, clue_syns, syn_noun, syn_verb, syn_adj, syn_adv):
    """
    Gives two scores to each word in the word list: One score is the path similarity on WordNet and the other
    score is the Lesk algorithm score.
    :param word_list: the list of words to gives scores as solutions.
    :param length: the length of the wanted solution.
    :param context_words: a list of context words from the clue's synsets.
    :param clue_tokens: the list of non-stop words from the clue.
    :param clue_syns: a list of synsets from the clue.
    :return: Two dictionaries: One holds the score using path similarity for each words and the other holds the
    score using Lesk for each word.
    """
    output_verb = {}
    output_adj = {}
    output_adv = {}
    output_lesk = {}
    output_noun = {}

    for obj in word_list:
        if len(obj) == length or length == 0:
            sim = 0
            sim_verb = 0
            sim_noun = 0
            sim_adj = 0
            sim_adv = 0

            # iterate over all the synsets for every value and calculate the similarity between
            # the synset and the synsets from the clues
            for synset in list(wn.synsets(obj, pos=wn.VERB)):
                temp = 0
                for i, val in enumerate(syn_verb):
                    temp = temp + synset.path_similarity(val)
                sim_verb = max(temp, sim_verb)
            for synset in list(wn.synsets(obj, pos=wn.NOUN)):
                temp = 0
                for i, val in enumerate(syn_noun):
                    temp = temp + synset.path_similarity(val)
                sim_noun = max(temp, sim_noun)
            for synset in list(wn.synsets(obj, pos=wn.ADJ)):
                temp = 0
                for i, val in enumerate(syn_adj):
                    if synset.path_similarity(val):
                        temp = temp + synset.path_similarity(val)
                sim_adj = max(temp, sim_adj)
            for synset in list(wn.synsets(obj, pos=wn.ADV)):
                temp = 0
                for i, val in enumerate(syn_adv):
                    if synset.path_similarity(val):
                        temp = temp + synset.path_similarity(val)
                sim_adv = max(temp, sim_adv)

            # iterate over all the synsets for every value and find the definition.
            # Then calculate and find 2 intersections:
            # 1. between the definition and the words from the original clue
            # 2. between the defintion and the context words array above.
            for synset in list(wn.synsets(obj)):
                def_words = word_tokenize(synset.definition())
                def_words = list(set(def_words))
                def_words = _remove_non_alphabet(def_words)
                temp1 = set(clue_tokens).intersection(def_words)
                temp2 = set(context_words).intersection(def_words)
                temp1 = len(temp1) / len(clue_tokens)
                temp2 = len(temp2) / len(context_words)
                t = 0.75 * temp1 + 0.25 * temp2 # give more weight to similarity to the clue
                sim = max(t, sim)

            if sim > 0:
                output_lesk[obj] = sim
            if sim_verb > 0:
                output_verb[obj] = sim_verb
            if sim_noun > 0:
                output_noun[obj] = sim_noun
            if sim_adj > 0:
                output_adj[obj] = sim_adj
            if sim_adv > 0:
                output_adv[obj] = sim_adv
    return output_noun, output_verb, output_adj, output_adv, output_lesk