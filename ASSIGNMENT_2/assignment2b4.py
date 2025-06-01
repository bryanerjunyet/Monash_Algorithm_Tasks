class Node:
    """
    Node class used in the Trie structure.
    Each node has 27 children (0 = '$' terminal, 1-26 = 'a' to 'z').
    """
    def __init__(self, value=None, depth=0):
        self.children = [None] * 27
        self.value = value
        self.depth = depth


class Trie:
    """
    Trie structure to insert and store dictionary words with terminal markers.
    """
    def __init__(self):
        self.root = Node(depth=0)

    def get_index(self, char):
        # Converts 'a'-'z' to 1-26
        return ord(char) - ord('a') + 1

    def add_word(self, word, value=None):
        node = self.root
        depth = 1
        for letter in word:
            idx = self.get_index(letter)
            if node.children[idx] is None:
                node.children[idx] = Node(depth=depth)
            node = node.children[idx]
            depth += 1
        # Mark end of word with '$' at index 0
        if node.children[0] is None:
            node.children[0] = Node(depth=depth)
        node.children[0].value = value


class Bad_AI:
    """
    Main class for the assignment.
    - Builds Trie from list_words
    - Detects near-match words using check_word
    """

    def __init__(self, word_list):
        self.trie = Trie()
        word_index = 0
        for word in word_list:
            self.trie.add_word(word, word)
            word_index += 1  # optional, in case you'd want to store indices
        self.root = self.trie.root

    def get_index(self, char):
        # Converts 'a'-'z' to 1-26
        return ord(char) - ord('a') + 1


    def check_word(self, sus_word):
        """
        Returns a list of words from the Trie that differ by exactly one letter.
        """
        matches = []
        sus_size = len(sus_word)
        alphabet_size = 26  # 'a' to 'z'

        for i in range(sus_size):
            for alphabet_num in range(alphabet_size):
                node = self.root
                valid = True
                # Skip if the replacement is the same as the original letter
                if alphabet_num != self.get_index(sus_word[i]) - 1:
                    for j in range(sus_size):
                        if j == i:
                            idx = alphabet_num + 1
                        else:
                            idx = self.get_index(sus_word[j])
                        if node.children[idx] is None:
                            valid = False
                            break
                        node = node.children[idx]

                    # Check if this path leads to a valid word
                    if valid and node.children[0] is not None and node.children[0].value is not None:
                        matches.append(node.children[0].value)

        return matches
    


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

