class Node:
    """
    Node data structure
    """
    def _init_(self, data = None, level = None, size = 27):
        # terminal $ at index 0
        self.link = [None] * size
        # data payload
        self.data = data
        self.level = level


class Trie:
    def _init_(self):
        self.root = Node(level = 0)
    
    def insert(self, key, data = None):
        count_level = 1
        # begin from root
        current = self.root
        # go through character(key) one by one
        for char in key:
            # calculate index for character
            # $ = 0, a = 1, b = 2, ..., z = 26
            index = ord(char) - ord('a') + 1
            # if pass exist continue, else create a new node
            if current.link[index] is not None:
                current = current.link[index]
            else:
                #create a new node
                current.link[index] = Node(level = count_level)
                current = current.link[index]
            count_level += 1
        index = 0 # terminal $ at index 0
        # go throught the terminal $
        if current.link[index] is not None:
                current = current.link[index]
        else:
            #create a new node
            current.link[index] = Node(level = count_level)
            current = current.link[index]
        current.data = data

    def search(self, key):
        # begin from root
        current = self.root
        # go through character(key) one by one
        for char in key:
            print(current.level)
            # calculate index for character
            # $ = 0, a = 1, b = 2, ..., z = 26
            index = ord(char) - ord('a') + 1
            # if pass exist continue, else create a new node
            if current.link[index] is not None:
                current = current.link[index]
            # if pass does not exist return None 
            else:
                #create a new node
                raise Exception(str(key) + " does not exist")
        index = 0 # terminal $ at index 0
        print(current.level)
         # go throught the terminal $
        if current.link[index] is not None:
            current = current.link[index]
        else:
            raise Exception(str(key) + " does not exist")
        print(current.level)
        return current.data