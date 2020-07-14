class SolutionFormat:
    """"
    Object that represents the known format of a solution to a clue. It includes the number of words and the length of
    each word in the solution, as well as a list of known letters.
    """

    def __init__(self, words, lengths, solution_format):
        self.num_of_words = words
        self.lengths = lengths
        self.total = sum(lengths)
        self.letters = self._parse_format(solution_format)

    def _parse_format(self, solution_format):
        """
        Function that parses a given format. The format is given as a string containing '_' (underscore) for unknown
        letters, the letters where they are known, and a ' ' (space) between words.
        """
        letters = {}

        if solution_format == "":
            return letters

        # Check number of words
        split_format = solution_format.split(" ")
        if not len(split_format) == self.num_of_words:
            raise ValueError()

        # Parse each word separately
        for i in range(len(split_format)):
            # Check number of letters in the word
            word_format = split_format[i]
            if not len(word_format) == self.lengths[i]:
                raise ValueError()

            # Parse the word
            for j in range(len(word_format)):
                if word_format[j].isalpha():
                    letters[(i, j)] = word_format[j]
                elif not word_format[j] == '_':
                    raise ValueError()

        return letters

    def add_spaces(self, word):
        """
        Given a string this function adds spaces between words such that the string would fit the solution format.
        If the total length of the string is not equal to the total length of the format, it is unchanged.
        """
        if self.num_of_words == 1:
            # Can't add spaces to one word
            return word

        if not len(word) == self.total:
            # Total length is incompatible
            return word

        # Iterate over all substrings in the string and concatenate them with spaces
        start = 0
        end = self.lengths[0]
        j = 1
        spaced = ""

        while j < self.num_of_words:
            spaced += word[start:end] + " "
            start = end
            end = self.lengths[j]
            j += 1

        spaced += word[end:]
        return spaced

    def check(self, word):
        """
        Function that checks if the given word in compatible with the format
        """
        spaced = self.add_spaces(word)
        words = spaced.split(" ")

        # Check number of words
        if not len(words) == self.num_of_words:
            return False

        # Check each word
        for i in range(len(words)):
            word = words[i]
            if not len(word) == self.lengths[i]:
                return False

            # Check that all letters are correct
            for j in range(len(word)):
                if (i, j) in self.letters.keys():
                    if not word[j] == self.letters[(i, j)]:
                        return False

        return True

    def get_total_length(self, spaces=False):
        if spaces:
            return self.total + self.num_of_words - 1
        else:
            return self.total
