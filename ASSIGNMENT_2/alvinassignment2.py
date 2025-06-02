"""
1. A Crowded Campus 
"""
from queue import Queue

class Edge:
    """
    Edge class for storing directed edge with capacity and flow.
    """
    def __init__(self, to, capacity):
        """
        Function description:
        Initializes an edge with a target node, capacity, and flow set to 0.

        :Input:
        to: target node id
        capacity: the max capacity of the edge

        :Output, return or postcondition:
        An edge object with set capacity and initialized flow.

        :Time complexity:
        O(1)

        :Time complexity analysis:
        Initialisation take constant time

        :Space complexity:
        O(1)

        :Space complexity analysis:
        constant space for edge with attributes to, capacity, flow, and rev.
        """
        self.to = to    # Target node ID
        self.capacity = capacity    # Maximum capacity of the edge
        self.flow = 0   # Current flow through the edge
        self.rev = None  # Reverse edge for residual graph


class NetworkFlow:
    """
    NetworkFlow class to represent a flow network using adjacency list representation.
    """
    def __init__(self, size):
        """
        Function description:
        Initializes the network with given number of nodes and adjacency lists.

        :Input:
        size: number of nodes in the network

        :Output, return or postcondition:
        A NetworkFlow object with all nodes and edge lists initialized.

        :Time complexity:
        O(V)

        :Time complexity analysis:
        Let V = number of nodes.
        - For loop to create adjacency list take linear time.

        :Space complexity:
        O(V)

        :Space complexity analysis:
        Let V = number of nodes.
        - Storage for adjacency list has size V.
        """
        self.size = size

        # Adjacency list for storing edges
        self.graph = []
        for _ in range(size):
            self.graph.append([])

    def add_edge(self, from_node, to_node, capacity):
        """
        Function description:
        Adds a directed edge from node u to v with a specified capacity.

        :Input:
        from_node: start node
        to_node: end node
        capacity: capacity of the edge

        :Output, return or postcondition:
        Modifies graph with new forward and reverse edge (for residual capacity).

        :Time complexity:
        O(1)

        :Time complexity analysis:
        Insertion into adjacency lists take constant time.

        :Space complexity:
        O(1)

        :Space complexity analysis:
        Constant space for creating a new edge and adding it to the adjacency list.
        """
        forward = Edge(to_node, capacity) # Forward edge from u to v with given capacity
        backward = Edge(from_node, 0)   # Reverse edge with 0 initial capacity
        forward.rev = backward  # Linking forward and backward edges
        backward.rev = forward
        self.graph[from_node].append(forward)   # Add to u's adjacency list
        self.graph[to_node].append(backward)  # Add reverse to v's adjacency list

    def bfs(self, source, sink, parent):
        """
        Function description:
        Standard BFS to find an augmenting path from s to t.

        :Input:
        source: source node
        sink: sink node
        parent: list to store the path

        :Output, return or postcondition:
        Returns True if path found, else False. Updates parent path.

        :Time complexity:
        O(V + E)

        :Time complexity analysis:
        Let V = number of vertices 
        Let E = number of edges.
        - Every node and edge in the level graph is processed once.

        :Space complexity:
        O(V)

        :Space complexity analysis:
        Let V = number of vertices 
        - Visited list and queue take O(V) space.
        """
        visited = [False] * self.size
        queue = Queue()
        queue.put(source)
        visited[source] = True
        while not queue.empty():
            current_node = queue.get()
            for edge in self.graph[current_node]:
                # Check for available capacity and if node has been visited
                if not visited[edge.to] and edge.capacity - edge.flow > 0:
                    visited[edge.to] = True
                    parent[edge.to] = (current_node, edge)
                    if edge.to == sink:
                        return True
                    queue.put(edge.to)
        return False

    def ford_fulkerson(self, source, sink):
        """
        Function description:
        Computes the maximum flow from the source node to the sink node using the 
        Ford-Fulkerson algorithm with BFS to find augmenting paths.

        :Input:
        source: The source node in the flow network.
        sink: The sink node in the flow network.

        :Output:
        Returns the total flow value sent from source to sink.

        :Time complexity:
        O(N^2)

        :Time complexity analysis:
        Let V = number of nodes in the flow network.
        Let E = number of edges in the flow network.
        Let N = number of students
        Let M = number of classes
        For each augmenting path, BFS runs in O(V + E) time.
        V(nodes) = O(N + M) 
        E(edges) = O(N + M)
        Total flow pushed: At most N units (each student can send at most 1 unit).
        Total time complexity = O(N(N+M)) = O(N^2) in the worst case since M is bounded by N.

        :Space complexity:
        O(N)

        :Space complexity analysis:
        Let N = number of nodes in the flow network.
        - BFS uses a visited array and a parent list, both of size O(N).
        """
        flow = 0
        parent = [None] * self.size

        # While there is an augmenting path from source to sink
        while self.bfs(source, sink, parent):
            path_flow = float('inf')
            current = sink

            # Find the minimum residual capacity along the path
            while current != source:
                previous, edge = parent[current]
                path_flow = min(path_flow, (edge.capacity - edge.flow))
                current = previous
            current = sink

            # Update the flow along the path
            while current != source:
                previous, edge = parent[current]
                edge.flow += path_flow
                edge.rev.flow -= path_flow
                current = previous
            flow += path_flow

        return flow

def crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction):
    """
    Function description:
    This function returns an allocation of each student to a proposed class. 
    The returned allocation satisfy the following requirements:
    - Each student is allocated to exactly one class.
    - Each proposed class satisfies its space occupancy constraints.
    - At least minimumSatisfaction students get allocated to classes with class times that are
    within their top 5 preferred time slots.
    
    Approach description:
    0. I assign unique indexes to students and classes in teh network, and created extra nodes for source, sink, satisfaction filter, overflow, and super sink.
    1. I added edges from the source to each student node, make sure each student sends out 1 unit of flow.
    2. I connected each student to their top 5 preferred time slots, allowing them to send flow to those time slots.
    3. Each time slot node connects to the class node, allowing flow from time slot to class.
    4. Each student node also connects to an overflow node, which allows them to send flow if they cannot be satisfied.
    5. The overflow node connects to a satisfaction filter node, which allows that at least 'minimumSatisfaction' students use their top 5 preferred time slots.
    6. The satisfaction filter node connected to every class node, allow non-preferred paths to be completed.
    7. Each class node has two out-edges:
        - one to the regular sink with capacity (max - min) 
        - one to a super sink with minimum required capacity.
    8. Lastly, the sink node connects to the super sink with capacity (n - total minimum required capacity), ensuring that the total flow matches the number of students.
    9. I run the Ford-Fulkerson algorithm to find the maximum flow from source to super sink.
    10. If flow successfully reaches n, I reconstruct the allocation by checking the flow values in the network along student -> time slot -> class edges.
        Remaining students are matched using overflow -> filter -> class edges.
    11. Finally, I check if all students were assigned to classes and if each class satisfies its capacity constraints.
        If any of these conditions are not met, I return None.


    :Input:
    n: Number of students
    m: Number of proposed classes
    timePreferences: List of lists, where each inner list contains the top 20 preferred time slots for each student.
    proposedClasses: List of lists, where each inner list contains the time slot, minimum capacity, and maximum capacity for each proposed class.
    minimumSatisfaction: Minimum number of students that should be satisfied with their top 5 preferred time slots.

    :Output, return or postcondition:
    Returns a list of class allocations, where each index corresponds to a student and the value is the class they are assigned to.
    If no valid allocation exists, returns None.

    :Time complexity:
    O(N^2)

    :Time complexity analysis:
        Let V = number of nodes in the flow network.
        Let E = number of edges in the flow network.
        Let N = number of students
        Let M = number of classes
        Let P = number of time preferences per student (fixed at 20).
    1. Graph construction:
        - Source to students: O(N)
        - Students to top 5 preferences: 5 per student = O(5N) = O(N)
        - Time slots to classes: O(M)
        - Students to overflow: O(N)
        - Overflow to satisfaction filter: O(1)
        - Satisfaction filter to classes: O(M)
        - Classes to sink: O(M)
        - Classes to super sink: O(M)
        - Sink to super sink: O(1)
        Total edges = O(N + M)
        P is constant (20)
    2. Ford-Fulkerson Max Flow:
        - For each augmenting path, BFS runs in O(V + E) time.
            - V(nodes) = O(N + M) 
            - E(edges) = O(N + M)
            - Total flow pushed: At most N units (each student can send at most 1 unit).
        Total time complexity = O(N(N+M)) = O(N^2) in the worst case since M is bounded by N.
    3. Reconstructing allocation:
        - Loop through students and check edges = O(N), each edge check is O(1)
        - Loop through overflow paths and check edges = O(NM) = O(N^2) as M is bounded by N.
        Total time complexity = O(N + N^2) = O(N^2).
    4. Validation of allocation:
        - Check if all students were assigned: O(N)
        - Check class capacity constraints: O(M)
        Total time complexity = O(N + M)

    Total time complexity is O(N^2) since M is bounded by N.
    
    :Space complexity:
    O(N)

    :Space complexity analysis:
    - Let N = number of students.
    - Let M = number of classes.
    1. Graph Representation:
        - Graph has O(N + M) nodes and edges.
        - Each edge is stored with forward and backward edges = O(N + M).
        - Adjacency list and edge = O(N + M)
    2. BFS:
        - During each BFS, O(N+M) for visited and parent arrays.
    3. Allocation list: O(N)
    4. Class counts: O(M)

    Total space complexity is O(N + M),
    since M <= N (M is bounded by N), we can simplify to O(N).
    
    """
    # Total number of time slots preference
    time_pref_count = 20

    # Node indexes in the flow network
    source = 0
    student_start_index = 1
    time_start_index = student_start_index + n
    class_start_index = time_start_index + time_pref_count
    satisfaction_overflow_node = class_start_index + m
    satisfaction_filter_node = satisfaction_overflow_node + 1
    sink_node = satisfaction_filter_node + 1
    super_sink_node = sink_node + 1
    total_nodes = super_sink_node + 1

    # Initialize the flow network
    flow = NetworkFlow(total_nodes)

    # 1. Source -> Students (Each student sends 1 unit of flow)
    for number_student in range(n):
        flow.add_edge(source, student_start_index + number_student, 1)

    # 2. Students -> Time Slots (Top 5 preferences)
    for number_student in range(n):
        student_node = student_start_index + number_student
        for pref in timePreferences[number_student][:5]:
            if 0 <= pref < time_pref_count:
                flow.add_edge(student_node, time_start_index + pref, 1)

    # 3. Time Slots -> Classes (Proposed classes)
    for number_class in range(m):
        proposed_time = proposedClasses[number_class][0]
        if not (0 <= proposed_time < time_pref_count):
            continue  # skip invalid time slot
        time_node = time_start_index + proposed_time
        class_node = class_start_index + number_class
        flow.add_edge(time_node, class_node, n)

    # 4. Students -> Overflow (if not satisfied)
    for number_student in range(n):
        flow.add_edge(student_start_index + number_student, satisfaction_overflow_node, 1)

    # 5. Overflow -> Satisfaction Filter (minimum satisfaction requirement)
    remaining_students = n - minimumSatisfaction
    flow.add_edge(satisfaction_overflow_node, satisfaction_filter_node, remaining_students)

    # 6. Satisfaction Filter -> Classes (allow overflow to classes)
    for number_class in range(m):
        flow.add_edge(satisfaction_filter_node, class_start_index + number_class, n)

    # 7. Classes -> Sink (max capacity minus min capacity)
    for number_class in range(m):
        max_cap = proposedClasses[number_class][2]
        min_cap = proposedClasses[number_class][1]
        cap_diff = max_cap - min_cap
        flow.add_edge(class_start_index + number_class, sink_node, cap_diff)

    # Classes -> Super Sink (minimum required capacity)
    for number_class in range(m):
        min_cap = proposedClasses[number_class][1]
        flow.add_edge(class_start_index + number_class, super_sink_node, min_cap)

    # 8. Sink -> Super Sink (to ensure total flow matches number of students)
    total_min_capacity = 0
    for j in range(m):
        class_min_capacity = proposedClasses[j][1]
        total_min_capacity += class_min_capacity
    remaining_capacity = n - total_min_capacity
    flow.add_edge(sink_node, super_sink_node, remaining_capacity)

    # 9. Run Ford-Fulkerson to find maximum flow
    total_flow = flow.ford_fulkerson(source, super_sink_node)
    if total_flow < n:
        return None
    
    # Reconstruct the allocation from the flow network
    allocation = [None] * n
    
    # 10. First pass: Preferred path (Check student -> time slot -> class edges)
    for number_student in range(n):
        student_node = student_start_index + number_student
        allocate_flag = False
        for edge in flow.graph[student_node]:
            # Check if student went through a time slot
            if (time_start_index <= edge.to < (time_start_index + time_pref_count)) and edge.flow > 0:
                time_node = edge.to
                time_slot = time_node - time_start_index
                # Check class edges from this time node
                
                for class_edge in flow.graph[time_node]:
                    if (class_start_index <= class_edge.to < (class_start_index + m)) and class_edge.flow > 0:
                        class_id = class_edge.to - class_start_index
                        if proposedClasses[class_id][0] == time_slot:
                            # Assign student and decrement flow to prevent double use
                            allocation[number_student] = class_id
                            class_edge.flow -= 1
                            edge.flow -= 1
                            allocate_flag = True
                            break

                if allocate_flag:
                    break

    
    # Second pass: Overflow path (Check students who were not assigned)
    for number_student in range(n):
        if allocation[number_student] is None:
            student_node = student_start_index + number_student
            for edge in flow.graph[student_node]:
                # Check if student went through overflow path
                if (edge.to == satisfaction_overflow_node) and edge.flow > 0:
                    # Follow sat_overflow -> sat_filter -> class path
                    
                    for sat_edge in flow.graph[satisfaction_overflow_node]:
                        if (sat_edge.to == satisfaction_filter_node) and sat_edge.flow > 0:
                            
                            for class_edge in flow.graph[satisfaction_filter_node]:
                                if (class_start_index <= class_edge.to < (class_start_index + m)) and class_edge.flow > 0:
                                    class_id = class_edge.to - class_start_index
                                    allocation[number_student] = class_id
                                    # Reduce flow to prevent double assignment
                                    sat_edge.flow -= 1
                                    class_edge.flow -= 1
                                    break
                            break

                    if allocation[number_student] is not None:
                        break
    
    # 11. Check if all students were assigned
    if None in allocation:
        return None
    
    # Check class capacity constraints
    class_counts = [0] * m
    for class_id in allocation:
        class_counts[class_id] += 1
    
    # Ensure each class meets its min and max capacity constraints
    for number_class in range(m):
        min_cap, max_cap = proposedClasses[number_class][1], proposedClasses[number_class][2]
        if not (min_cap <= class_counts[number_class] <= max_cap):
            return None
    
    return allocation





"""
2. Typo
"""

class TrieNode:
    """
    Node class for Trie with fixed array links.
    """
    def __init__(self, data=None):
        """    
        Function description:
        Initializes a Trie node with fixed-size array links for 27 characters (0 for '$', 1-26 for 'a'-'z').
        
        :Input:
        data: Data to store in the node (the word itself).

        :Output, return or postcondition:
        - Creates a node with an array of links initialized to None, ready to store child nodes.

        :Time complexity:
        O(1)
        :Time complexity analysis:
        - The initialization of the fixed-size array and data is done in constant time.
        - The size of the array is fixed at 27, so it does not depend on the input size.

        :Space complexity:
        O(1)
        :Space complexity analysis:
        - The space used by the node is constant, as it always contains a fixed-size array of links.
        """
        self.link = [None] * 27  # link[0] is for terminal '$', link[1] to link[26] for 'a' to 'z'
        self.data = data
        self.length = 0


class Trie:
    """
    Trie class for storing words with fixed-size array links.
    """
    def __init__(self):
        """
        Function description:
        Initializes a Trie with a root node.

        :Input:
        None

        :Output, return or postcondition:
        Creates a root node with fixed-size array links, ready to store words.

        :Time complexity:
        O(1)
        :Time complexity analysis:
        - The initialization of the root node is done in constant time.

        :Space complexity:
        O(1)
        :Space complexity analysis:
        - The space used by the root node is constant, as it always contains a fixed-size array of links.
        """
        self.root = TrieNode()

    def insert(self, key, data=None):
        """
        Function description:
        Inserts a single word into the trie, marking the final character a terminal node.

        :Input:
        key: The word to be inserted into the trie.
        data: Optional data to store in the terminal node (usually the word itself).

        :Output, return or postcondition:
        The trie now contains the word, accessible through traversal.

        :Time complexity:
        O(M)

        :Time complexity analysis:
        - Let M = length of the word being inserted.
        - Each character in the word is processed once, leading to O(M) time complexity.

        :Space complexity:
        O(M)

        :Space complexity analysis:
        In the worst case, every character in key creates a new node.
        """
        current = self.root
        length = len(key)
        if length > self.root.length:
            self.root.length = length

        for char in key:
            index = ord(char) - ord('a') + 1  # a=1, ..., z=26
            # if path exist does not exist, create a new node
            if current.link[index] is None:
                current.link[index] = TrieNode()
            current = current.link[index]
            # Update the length of the current node 
            if current.length < length:
                current.length = length

        terminal_index = 0  # terminal '$' at index 0
        # Add terminal marker '$' at index 0
        if current.link[terminal_index] is None:
            current.link[terminal_index] = TrieNode()

        current.link[terminal_index].data = data  # store the full word at terminal


class Bad_AI:
    """
    Bad AI class for checking words against a trie of known words.
    """
    def __init__(self, list_words):
        """
        Function description:
        Builds the Bad_AI object by creating an internal Trie and inserting all given words into it.

        Approach description:
        - A new Trie is created.
        - Each word in the input list is inserted into the Trie one by one.
        - Each insertion also stores the full word at the terminal marker node, which is used later for retrieval.
        - The insert operation ensures that all characters are mapped to fixed indices in the Trie using a 27-slot array for fast access.

        :Input:
        list_words: A list of lowercase words to preload into the Trie.

        :Output, return or postcondition:
        After initialization, all words from the list are stored in the Trie and are ready for search queries.

        :Time complexity:
        O(C)

        :Time complexity analysis:
        - Let C = total number of characters across all input words.
        - Each character is inserted into the Trie once per word, resulting in O(C) total time.

        :Space complexity:
        O(C)

        :Space complexity analysis:
        - Let C = total number of characters across all input words.
        - In the worst case, each unique character at each position creates a new Trie node.
        """
        self.trie = Trie()
        for word in list_words:
            self.trie.insert(word, word)

    def check_word(self, sus_word):
        """
        Function description:
        Checks for all words in the trie that differ from the given suspicious word ('sus_word') by exactly one character substitution. 

        Approach description:
        1. For each character position in the suspicious word, I attempt to substitute it with every other lowercase letter from 'a' to 'z', excluding the original character.

        2. For each substitution attempt, I perform a three-part traversal in the Trie:
        - First, I follow the prefix of the word up to (but not including) the substituted position using the original characters.
        - Next, I apply the substitution by stepping into the Trie using the new character at that position.
        - Then, I continue traversing the remaining suffix of the word using the original characters.

        3. If the traversal successfully reaches a terminal node after applying exactly one substitution, I collect the corresponding word stored at that terminal node into the result list.

        Input:
        - sus_word: A lowercase string (suspicious word) to be checked for typo.

        :Output, return or postcondition:
        - Returns a list of words from the trie that differ from 'sus_word' by exactly one substitution.

        :Time complexity:
        O(J * N) + O(X)

        -Time complexity analysis:
        - Let J = the length of the sus word.
        - Let N = the number of words stored in the trie (from list_words).
        - Let X = total number of characters in the result list.
        - In the worst case, I try J positions * 25 substitutions, and each substitution could touch nodes 
        along paths for many of the N words, so it's O(J * N) for the traversal.
        - Collecting the results costs O(X), where X is the total number of characters in the result list.

        Space complexity:
        O(X)

        Space complexity analysis:
        - Let X = total number of characters in the result list.
        - The traversal only uses a few constant variable, so fixed space.
        - The only thing that grows is the list of returned words, which is O(X) total characters.
        """
        # Initialize result list to collect matching words
        result = []
        sus_word_length = len(sus_word)
        char_a = ord('a')  # ASCII value of 'a'
        root = self.trie.root

        # If sus_word is longer than anything in the trie, skip early
        if sus_word_length > root.length:
            return result

        # Iterate over each position in the suspect word
        for position in range(sus_word_length):
            original_index = ord(sus_word[position]) - char_a + 1

            # Try all possible substitutions except the original character
            for substitute_character in range(1, 27):
                if substitute_character == original_index:
                    continue  # Skip the same character

                current_node = root
                same_character_flag = True

                # Follow trie for the prefix part (before i)
                for i in range(position):
                    character = ord(sus_word[i]) - char_a + 1
                    current_node = current_node.link[character]
                    if current_node is None or current_node.length < sus_word_length:
                        same_character_flag = False
                        break
                
                # Skip if prefix traversal failed
                if not same_character_flag:
                    continue

                # Apply the character substitution at position i
                current_node = current_node.link[substitute_character]
                if current_node is None or current_node.length < sus_word_length:
                    continue

                # Follow the rest of the word after the substituted char
                for i in range(position + 1, sus_word_length):
                    character = ord(sus_word[i]) - ord('a') + 1
                    current_node = current_node.link[character]
                    if current_node is None or current_node.length < sus_word_length:
                        same_character_flag = False
                        break

                # Skip if the suffix traversal failed
                if not same_character_flag:
                    continue

                # If we reach a terminal node, it's a valid match
                terminal_node = current_node.link[0]
                if terminal_node is not None and len(terminal_node.data) == sus_word_length:
                    result.append(terminal_node.data)

        return result
