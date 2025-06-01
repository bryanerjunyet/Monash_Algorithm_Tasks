class Node:
    """
    Node class for Trie implementation
    Each node contains:
    - links: array of size 27 (a-z + terminal $)
    - word: stores the complete word at terminal node
    """
    def __init__(self):
        self.links = [None] * 27  # index 0 for terminal, 1-26 for a-z
        self.word = None  # stores the complete word at terminal node


class Bad_AI:
    """
    Class to efficiently find words with Levenshtein distance of exactly 1 (substitutions only)
    """
    def __init__(self, list_words):
        """
        Initialize the Bad_AI with a list of words by building a trie
        :Input: 
            list_words: list of strings to be stored in the trie
        :Time complexity: O(C) where C is total characters in list_words
        :Space complexity: O(C) for storing the trie
        """
        self.root = Node()
        for word in list_words:
            self._insert(word)

    def _get_index(self, char):
        """
        Helper function to convert character to trie index
        a->1, b->2, ..., z->26, $->0
        """
        if char == '$':
            return 0
        return ord(char) - ord('a') + 1

    def _insert(self, word):
        """
        Insert a word into the trie
        :Input: word to be inserted
        :Time complexity: O(M) where M is length of word
        """
        current = self.root
        for char in word:
            index = self._get_index(char)
            if current.links[index] is None:
                current.links[index] = Node()
            current = current.links[index]
        # Mark terminal node with complete word
        terminal_index = self._get_index('$')
        if current.links[terminal_index] is None:
            current.links[terminal_index] = Node()
        current.links[terminal_index].word = word

    def check_word(self, sus_word):
        """
        Find all words in trie that are exactly one substitution away from sus_word
        :Input: 
            sus_word: suspicious word to compare against
        :Output: 
            list of words with Levenshtein distance 1 (substitutions only)
        :Time complexity: O(J*N) + O(X) where J is length of sus_word, 
                          N is number of words, X is output size
        :Space complexity: O(X) for storing results
        """
        result = []
        J = len(sus_word)
        char_array = [char for char in sus_word]  # Convert to list for mutability
        
        # For each character position in sus_word
        for i in range(J):
            original_char = sus_word[i]
            
            # Try replacing with every possible letter (a-z)
            for replacement in range(26):
                replacement_char = chr(ord('a') + replacement)
                
                # Skip if replacement is same as original
                if replacement_char == original_char:
                    continue
                
                # Modify the character at position i
                char_array[i] = replacement_char
                
                # Search for this modified word in trie
                current = self.root
                found = True
                for char in char_array:
                    index = self._get_index(char)
                    if current.links[index] is None:
                        found = False
                        break
                    current = current.links[index]
                
                # Check terminal node
                if found:
                    terminal_index = self._get_index('$')
                    if (current.links[terminal_index] is not None and current.links[terminal_index].word is not None):
                        result.append(current.links[terminal_index].word)
                
                # Restore original character
                char_array[i] = original_char
        
        return result


if __name__ == "__main__":
    # Test cases from assignment example
    list_words = ["aaa", "abc", "xyz", "aba", "aaaa"]
    list_sus = ["aaa", "axa", "ab", "xxx", "aaab"]
    my_ai = Bad_AI(list_words)
    
    expected_results = [
        ["aba"],
        ["aaa","aba"],
        [],
        [],
        ["aaaa"]
    ]
    
    # Run tests and verify
    for i, sus_word in enumerate(list_sus):
        result = my_ai.check_word(sus_word)
        print(f"Input: {sus_word}, Output: {result}")
        assert sorted(result) == sorted(expected_results[i]), f"Test failed for {sus_word}"
    
    print("All test cases passed!")