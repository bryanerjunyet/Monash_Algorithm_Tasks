"""
:Module description:
This module is a program for user to identify input words that have exactly 
one character substitution (Levenshtein distance of one) from the words in a
given dictionary. A Trie-based solution is implemented to efficiently store all 
dictionary words and optimise search process efficient lookup time by the Trie data structure.

:Classes:
Node    : A single Trie node that contains a complete word and character links.
Bad_AI  : A Trie for efficient searching of words with one character substitution from the given dictionary. 

"""

__author__ = "Er Jun Yet"



class Node:
    """
    This class represents a single node in a Trie data structure.
    """

    def __init__(self):
        """
        :Function description:
            A Node constructor with 27 character links and a complete word stored (if it is an end node).

        :Time complexity:
            O(1)

        :Time complexity analysis:
            Constant time for initialisation of Node attributes.
        
        :Space complexity:
            O(1)

        :Space complexity analysis:
            Constant space for input and auxiliary.

        """
        self.links = [None] * 27    # 26 spaces for a-z and terminal ($)
        self.word = None            # complete word stored at terminal node


    def get_word(self):
        """
        :Function description:
            Get the complete word stored in this node (if terminal node).

        :Output:
            str or None: The complete word stored at the terminal node or None (not a word).

        :Time complexity:
            O(1)

        :Time complexity analysis:
            Constant time to access the word attribute stored.

        :Space complexity:
            O(1)
        
        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

        """
        word_index = 0  # terminal index ($)
        if self.links[word_index] is not None: # word found
            return self.links[word_index].word
        else: # word not found
            return None 



class Bad_AI:
    """
    :Class description:
        This is the main class of the module that is a Bad AI tool that implements 
        a Trie-based approach identify input words that have exactly one character substitution 
        from the words in a given dictionary.
        
    :Approach description:
        The purpose of such Trie dictionary to be constructed allows efficient prefix-based searching
        of words. Below is an example of how the multiverse is constructed:
        
        Assume we have a dictionary of words "aaa", "aba" and "abc".
        Then, the Trie dictionary is constructed as follows:
        Root
        |--- a
             |
             |---- a
             |     |----- a (word: "aaa")
             |
             |---- b
                   |----- a (word: "aba")
                   |
                   |----- c (word: "abc")
        
        Therefore, once a word is inputted, each character position in the word is substituted with all possible 
        alphabets from a to z and checked against the Trie dictionary for any matches, else early termination 
        is introduced by the prefix check inherent in the Trie data structure.
        
    :Attributes:
        ALPHABETS   (str)   : Constant of all alphabets from a to z.
        root        (Node)  : Root node of the Trie data structure.
        
    """

    ALPHABETS = 'abcdefghijklmnopqrstuvwxyz'
    

    def __init__(self, list_words):
        """
        :Function description:
            A Bad_AI constructor that constructs a Trie dictionary from a given list of words.

        :Input:
            list_words (List[str]) : A list of real words in dictionary.

        :Time complexity:
            O(C), where C is the total number of characters across all input words.

        :Time complexity analysis:
            Linear time for adding each word to the Trie with add_word().

        :Space complexity:
            O(C), where C is the total number of characters across all input words.
        
        :Space complexity analysis: 
            Input space of O(C) for storing the list of words with number of chars, 
            and auxiliary space of O(C) for the Trie structure.

        """
        # Root node of the Trie
        self.root = Node()
        # Each word of each char in the Trie
        for word in list_words:
            self.add_word(word)
    

    def get_index(self, char):
        """
        :Function description:
            Get the corresponding character index in the links array of Node.

        :Input:
            char (str): A character.

        :Output:
            int: Corresponding character index.

        :Time complexity:
            O(1)
        
        :Time complexity analysis:
            Constant time to get the index of the character.

        :Space complexity:
            O(1)
        
        :Space complexity analysis:
            No additional space is used.

        """
        if char == '$':
            return 0
        else:
            return ord(char) - ord('a') + 1
    

    def add_word(self, word):
        """
        :Function description:
            Adds a word into the trie by creating nodes for each character.

        :Input:
            word (str): The word to insert.

        :Time complexity:
            O(M), where M is the number of characters in the word.
        
        :Time complexity analysis:
            Linear time for inserting each character Node of the word into the Trie.

        :Space complexity:
            O(M), where M is the number of characters in the word.
        
        :Space complexity analysis:
            Input space of O(M) for the characters being inserted, and auxiliary space of O(M) for the Trie structure.

        """
        current_node = self.root
        
        # Traverse through each character in the word
        for char in word:
            index = self.get_index(char)
            
            # Create a new node for new character
            if current_node.links[index] is None:
                current_node.links[index] = Node()
                current_node = self.next_char(current_node, index)
            else:
                current_node = self.next_char(current_node, index)

        # Store complete word at the terminal node
        word_index = self.get_index('$')
        if current_node.get_word() is None:
            current_node.links[word_index] = Node()
            current_node.links[word_index].word = word
        else:
            current_node.links[word_index].word = word


    def next_char(self, current_node, current_index):
        """
        :Function description:
            Traverse to next Node in Trie with links array.

        :Input:
            current_node (Node): Current node.
            current_index (int): Character index in links array.

        :Output:
            Node or None: The next node or None (no next node).

        :Time complexity:
            O(1)
        
        :Time complexity analysis:
            Constant time to traverse to the next node.

        :Space complexity:
            O(1)
        
        :Space complexity analysis:
            No additional space is used.

        """
        return current_node.links[current_index]
        

    def replace_char(self, sus_word, node_index, sus_index, new_char):
        """
        :Function description:
            Attempt to substitute a new character or still the original character.

        :Input:
            sus_word (str)  : Suspicious word.
            node_index (int): Current index in the traversal.
            sus_index (int) : Character substitution index.
            new_char (str)  : New character replaced.

        :Output:
            (int, str): Links array index and actual character used.

        :Time complexity:
            O(1)
        
        :Time complexity analysis:
            Constant time to determine the character and its index.

        :Space complexity:
            O(1)
        
        :Space complexity analysis:
            No additional space is used.
            
        """
        if node_index == sus_index:
            current_char = new_char
            current_index = self.get_index(current_char)
        else:
            current_char = sus_word[node_index]
            current_index = self.get_index(current_char)
        return current_index, current_char
    

    def check_word(self, sus_word):
        """
        Find all words that are one letter different from sus_word
        Time: O(J*N) where J is word length, N is number of words
        Space: O(X) where X is total letters in results
        """
        results = []
        sus_size = len(sus_word)
        trie_depth = len(sus_word)
        
        # Check each position in the word
        for sus_index in range(sus_size):
            original_char = sus_word[sus_index]
            
            # Try every possible letter replacement
            for new_char in self.ALPHABETS:
                if new_char != original_char:
                    # Start checking from the top of the tree
                    current_node = self.root
                    match = True
                    
                    # Check each character in the word
                    for node_index in range(trie_depth):
                        # If path doesn't exist, no match
                        current_index, current_char = self.replace_char(sus_word, node_index, sus_index, new_char)
                        if current_node.links[current_index] is not None:
                            current_node = self.next_char(current_node, current_index)                    
                        else:
                            match = False
                            current_node = self.next_char(current_node, current_index)  
                            break                  
                    # If we reached the end, check if it's a complete word
                    if match == True:
                        if (current_node.get_word() is not None):
                            results.append(current_node.get_word())
        
        return results


# Let's test it with the example from the assignment
if __name__ == "__main__":
    print("Testing our Bad_AI implementation:")
    
    # Our list of correct words
    correct_words = ["baa", "abc", "xyz", "aba", "aaaa"]
    
    # Words to check against
    test_words = ["aaa", "axa", "ab", "xxx", "aaab"]
    
    # Expected results
    expected = [
        ["aba"],
        ["aaa", "aba"],
        [],
        [],
        ["aaaa"]
    ]
    
    # Create our Bad_AI helper
    word_checker = Bad_AI(correct_words)
    
    # Test each case
    for i in range(len(test_words)):
        word = test_words[i]
        found = word_checker.check_word(word)
        print(f"Checking '{word}':")
        print(f"  Found: {found}")
        print(f"  Expected: {expected[i]}")
        print("  " + ("✓ Passed" if sorted(found) == sorted(expected[i]) else "✗ Failed"))
        print()