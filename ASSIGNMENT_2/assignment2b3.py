class Node:
    """
    Node for Trie data structure
    Each node contains:
    - links: array of size 27 (a-z + terminal $)
    - is_end: marks if this node is the end of a word
    """
    def __init__(self):
        self.links = [None] * 27
        self.is_end = False

class Bad_AI:
    """
    Class to efficiently find words with Levenshtein distance of 1 (substitutions only)
    """
    def __init__(self, list_words):
        """
        Initializes the Bad_AI with a list of words.
        Builds a trie structure and groups words by length.
        
        Time complexity: O(C) where C is total characters in list_words
        Space complexity: O(C) for storing the trie
        """
        self.root = Node()
        self.words_by_length = [[] for _ in range(101)]  # Assuming max word length 100
        
        for word in list_words:
            length = len(word)
            self.words_by_length[length].append(word)
            self._insert(word)
    
    def _insert(self, word):
        """
        Inserts a word into the trie.
        """
        current = self.root
        for char in word:
            index = ord(char) - ord('a') + 1
            if current.links[index] is None:
                current.links[index] = Node()
            current = current.links[index]
        current.is_end = True
    
    def check_word(self, sus_word):
        """
        Finds all words in the dictionary that are exactly one substitution away from sus_word.
        
        Time complexity: O(J*N) + O(X) where:
        - J is length of sus_word
        - N is number of words with same length as sus_word
        - X is total characters in output
        
        Space complexity: O(X) for the output
        """
        result = []
        word_len = len(sus_word)
        same_length_words = self.words_by_length[word_len]
        
        for word in same_length_words:
            diff = 0
            for i in range(word_len):
                if word[i] != sus_word[i]:
                    diff += 1
                    if diff > 1:
                        break
            if diff == 1:
                result.append(word)
        
        return result