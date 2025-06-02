"""
===========================================================================================================

**** TASK 1 - A Crowded Campus ****

:Module description (Part 1):
This module section is a program for campus to allocate students to classes based on the physical class 
capacities and availability as well as student's preferred time. A Flow-Network-based approach is implemented
to model the allocation process to achieve the best proposed allocation of classes to students, where a minimum
satisfaction number of students obtain one of their top 5 preferred time slot, each student is allocated to 
exactly one class and each class meets its minimum and maximum capacity. 

:Classes:
AllocationFlow    : A flow edge in the AllocationNetwork represents a possible assignment to a decision point.
AllocationPoint   : A node in the AllocationNetwork represents a decision point in the allocation process.
AllocationNetwork : A manager class for AllocationNetwork construction and flow processing.

===========================================================================================================
"""

__author__ = "Er Jun Yet"


import queue

class AllocationNetwork:
    """
    :Class description:
        This is the main class of the program that act as a manager class for construction of the AllocationNetwork
        and processing of allocation flow through the network flow.

    :Approach description:
        The purpose of implementing such allocation with Flow Network allows for best and effective proposed allocation 
        of classes to students, especially in this case where there is a demand on the class capacity and student time 
        preferences. A Flow-Network-based approach owns a perfect solution to resolve this student-class allocation problem
        efficiently by transforming students as flow units flowing through a network of connections or edges with restricted 
        capacities in our AllocationNetwork from a source node to a sink node, where each student chooses only one decision path
        to choose their class. 

        The AllocationNetwork is designed meticulously with a layered structure of allocation process with multiple allocation points 
        and layered capacity constraints. The network mainly consists of the following allocation points (nodes):
        1. A source node
        2. Multiple student nodes (one for each student)
        3. Multiple time nodes (5 preferred time slots for each student)
        4. Multiple class nodes (one for each corresponding classes)
        5. Two alternative nodes (for alternative allocation for students did not choose time preference)
        6. A sink node (for remaining flow of students to achieve maximum class capacity)
        7. A super sink node (for minimum flow of students to achieve minimum class capacity)

        Below is a rough example of how the AllocationNetwork is constructed:
        [only for illustration purpose, minor inaccuracy in representation of connection details, further details are explained below]

                            capacity=1            capacity=n
                                    ---> (T1) ---------------------> (C1) ---------------------------------------------------------        
                                    |                            |                 |                                              |
                                    |                            |                 |                                              |
                                    |--> (T2) -------------------|-> (C2) ---------|----------------------------------------------|
                                    |                            |                 |                                              |
            capacity=1              |                            |                 |                                              |
                -------> (S1) ------|--> (T3) -------------------|-> (C3) ---------|----------------------------------------------|
                |               |   |                            |                 |                                              |
                |               |   |                            |                 |                                              |
                |               |   |--> (T4) -------------------|-> (C4) ---------|----------------------------------------------|
                |               |   |                            |                 |                                              |
                |               |   |                            |                 |                                              |
                |               |   ---> (T5) -------------------|-> (C5) ---------|----------------------------------------------|
                |   capacity=1  |                   capacity=n   |                 |                                              |    
                |               |   ---> (T6) -------------------|-> (C6) ---------|----------------------------------------------|     
                |               |   |                            |                 |                                              |
                |               |   |                            |                 |                                              |
                |               |   |--> (T7) -------------------|-> (C7) ---------|----------------------------------------------|
                |               |   |                            |                 | capacity              capacity               |
                |               |   |                            |                 | = max_cap - min_cap   = sum_min_cap          |
    [SOURCE]----|------> (S2) --|---|--> (T8) -------------------|-> (C8) ---------|-----------> [SINK] --------> [SUPER SINK] <--| capacity = min_cap
                |               |   |                            |                 |         {FOR REMAINING FLOW}                 | {FOR MINIMUM FLOW}
                |               |   |                            |                 |                                              |
                |               |   |--> (T9) -------------------|-> (C9) ---------|----------------------------------------------| 
                |               |   |                            |                 |                                              |
                |               |   |                            |                 |                                              |
                |   capacity=1  |   ---> (T10) ------------------|-> (C10) --------|----------------------------------------------| 
                |               |                  capacity=n    |                 |                                              |
                |               |   ---> (T11) ------------------|-> (C11) --------|----------------------------------------------|        
                |               |   |                            |                 |                                              |
                |               |   |                            |                 |                                              |
                |               |   |--> (T12) ------------------|-> (C12) --------|----------------------------------------------|
                |               |   |                            |                 |                                              |
                |               |   |                            |                 |                                              |
                -------> (S3) --|---|--> (T13) ------------------|-> (C13) --------|----------------------------------------------|
            capacity=1          |   |                            |                 |                                              |
                                |   |                            |                 |                                              |
                                |   |--> (T14) ------------------|-> (C14) --------|----------------------------------------------|
                                |   |                            |                 |                                              |
                                |   |                            |                 |                                              |
                                |   ---> (T15) ------------------|-> (C15) --------------------------------------------------------
                                |                                |
                     capacity=1 |                                | capacity=n
                                |                                |
                                |                                |
                                --------> [ALT1] ----> [ALT2] ----
                                            capacity = n-minimumSatisfaction

            *** LEGEND: ***
            [SOURCE]        = Source node
            [SINK]          = Sink node
            [SUPER SINK]    = Super Sink node
            (S1)            = Student 1 node
            (T1)            = Time 1 node
            (C1)            = Class 1 node
            (ALT1)          = Alternative 1 node
            (ALT2)          = Alternative 2 node


        To begin with, source node connects all student nodes with exactly one flow unit (capacity = 1), representing each student 
        must be assigned once. Secondly, all student nodes connect to five time nodes (capacity = 1), representing their top 5 preferred time slots 
        (only 1 can be chosen). Next up, time nodes connect to their corresponding classes (capacity = n, where n is the number of students), 
        representing multiple students to select classes. Alternatively, all student nodes also connect to alternative nodes, ALT1 and ALT2,
        where ALT1 bypasses students with not chosen or not allocated with time preferences (capacity = n - minimumSatisfaction) and connect 
        directly to classes, while ALT2 serves as an overflow node (capacity = n). Finally, all class nodes divide connections into two flows,
        one to super sink node that flows minimum students (capacity = minimum class capacity), and one to sink node that flows remaining students
        (capacity = maximum class capacity - minimum class capacity), then ultimately from sink node to super sink node (capacity = n - sum of all 
        minimum class capacity). Ultimately, Ford-Fulkerson algorithm is applied on this intricate design that guarantees the maximum flow of students
        to the best class allocation that satisfy all given constraints with minimum satisfaction number of students.
        
    """

    def __init__(self, students, classes):
        """
        :Function description:
            AllocationNetwork constructor to manage the construction and flow processing of Flow Network data structure.
            
        :Input:
            students (int)  : Number of students, n
            classes (int)   : Number of classes, m
            
        :Time complexity:
            O(N + M + C) --> O(N + M) --> O(N) 
            where N is the total number of students, M is the total number of classes and C is the total number of constant nodes.    
        
        :Time complexity analysis:
            Linear time for initialising all nodes in the AllocationNetwork, which consists of all students, time slots (5 for each student),
            classes and other constant nodes (source, sink, super sink, 2 alternative nodes). Since the number of students is more that th
            number of classes, where N >= M, N dominates the time complexity while the constant nodes do not affect the time complexity.
            Thus, the time complexity simplifies to O(N).
            
        :Space complexity:
            O(N + M + C) --> O(N + M) --> O(N) 
            where N is the total number of students, M is the total number of classes and C is the total number of constant nodes.    
        
        :Space complexity analysis:
            Input space of O(1) for the integer number of students and classes and auxiliary space of O(N + M + C) for the storing of all nodes
            in the AllocationNetwork, which consists of all students, time slots (5 for each student), classes and other constant nodes (source, sink,
            super sink, 2 alternative nodes). Since the number of students is more that the number of classes, where N >= M, N dominates the space
            complexity while the constant nodes do not affect the space complexity. 
            Thus, the space complexity simplifies to O(N).
            
        """
        # Constants for node identification numbers
        self.SOURCE = 0
        self.STUDENT_START = 1
        self.TIME_START = self.STUDENT_START + students
        self.CLASS_START = self.TIME_START + 20
        self.ALTERNATIVE1 = self.CLASS_START + classes
        self.ALTERNATIVE2 = self.ALTERNATIVE1 + 1
        self.SINK = self.ALTERNATIVE2 + 1
        self.SUPER_SINK = self.SINK + 1
        self.TOTAL_NODES = self.SUPER_SINK + 1

        # Initialisation of all nodes
        self.students = students
        self.classes = classes
        self.nodes = []
        for i in range(self.TOTAL_NODES):
            self.nodes.append(AllocationPoint(i))


    def add_connection(self, start, end, capacity):
        """
        :Function description:
            Connect two decision nodes in the AllocationNetwork with a forward and backward (residual) edge with given capacity.

        :Input:
            start    (int) : Start node identification number
            end      (int) : End node identification number
            capacity (int) : Maximum capacity of the forward edge

        :Time complexity:
            O(1)

        :Time complexity analysis:
            Constant time for adding a connection between two nodes in the AllocationNetwork.

        :Space complexity:
            O(1)

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

        """
        forward = AllocationFlow(start, end, capacity)
        backward = AllocationFlow(end, start, 0)
        forward.reverse = backward
        backward.reverse = forward
        self.nodes[start].connect(forward)
        self.nodes[end].connect(backward)
    

    def reset(self):
        """
        :Function description:
            Resets discovery flag and any incoming connection for BFS algorithm.
        
        :Time complexity:
            O(N), where N is the number of students.

        :Time complexity analysis:
            Linear time for resetting discovery flag and incoming connection for each node.
            Since N >= M, where N is the number of student nodes and M is the number of class nodes, 
            N dominates the time complexity and other constant nodes do not affect the time complexity.
            Thus, the time complexity simplifies to O(N).
        
        :Space complexity:
            O(1)

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

        """
        for node in self.nodes:
            node.discovered = False
            node.incoming_connection = None


    def breadth_first_search(self):
        """
        :Function description:
            Performs a Breadth First Search algorithm from source to super sink to find an augmenting path.

        :Output:
            bool: True if a path is found or not False.

        :Time complexity:
            O(N), where N is the number of students (student connections).

        :Time complexity analysis:
            Linear time for traversing all student connection edges in the AllocationNetwork (student connections dominate).

        :Space complexity:
            O(N), where N is the number of students (nodes).

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(N) for the storing of all nodes in Queue (student nodes dominate).

        """
        # Reset all node states
        self.reset()
        path = queue.Queue()
        source_node = self.nodes[self.SOURCE]
        source_node.discovered = True
        path.put(source_node)

        while not path.empty():
            # Current node to start
            start = path.get()
            if start.node_no != self.SUPER_SINK: # Still traversing nodes
                for connection in start.connections:
                    # Residual capacity check
                    residual = connection.capacity - connection.flow
                    if residual > 0:
                        end = self.nodes[connection.end]
                        if not end.discovered: # Track path
                            end.discovered = True
                            end.incoming_connection = connection
                            path.put(end)
            else: # Arrived at super sink, path found!
                return True
        return False


    def run_ford_fulkerson(self):
        """
        :Function description:
            Performs maximum flow from source node to the super sink node using Ford Fulkerson algorithm with BFS.

        :Output:
            int: Maximum flow from source node to super sink node

        :Time complexity:
            O(N^2), where N is the number of students (maximum flow).

        :Time complexity analysis:
            Linear time for each BFS search and the maximum number of augmenting paths is at most equal to the total flow, 
            which is bounded by the number of students.

        :Space complexity:
            O(N), where N is the number of students (nodes).

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(N) for the storing of nodes in the breadth_first_search().
            
        """
        max_flow = 0
        # Augmenting path exists
        while self.breadth_first_search():
            path_flow = float('inf')
            v = self.nodes[self.SUPER_SINK]
            # Search of minimum residual capacity
            while v.node_no != self.SOURCE:
                connection = v.incoming_connection
                path_flow = min(path_flow, connection.capacity - connection.flow)
                v = self.nodes[connection.start]
            # Update flow along the path
            v = self.nodes[self.SUPER_SINK]
            while v.node_no != self.SOURCE:
                connection = v.incoming_connection
                # Update forward and backward flow
                connection.flow += path_flow
                connection.reverse.flow -= path_flow
                v = self.nodes[connection.start]
            # Total flow accumulation
            max_flow += path_flow
        return max_flow


    def build_student_flow(self):
        """
        :Function description:
            Connects source node to each student node with capacity = 1.

        :Time complexity:
            O(N), where N is the number of students.

        :Time complexity analysis:
            Linear time for connecting source node to each student node.

        :Space complexity:
            O(1)

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

        """
        # Connect each student
        for i in range(self.students):
            self.add_connection(self.SOURCE, self.STUDENT_START + i, 1)


    def build_time_flow(self, timePreferences):
        """
        :Function description:
            Connects each student node to 5 time nodes with capacity = 1.

        :Input:
            timePreferences (List[List[int]]): List of preferred time slots from student.

        :Time complexity:
            O(N), where N is the number of students.

        :Time complexity analysis:
            Linear time for connecting each student node to 5 time nodes, resulting in O(5N),
            where connections of 5 time nodes is constant.

        :Space complexity:
            O(1)

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).
            
        """
        # Connect each student
        for i in range(self.students):
            student_node = self.STUDENT_START + i
            # Connect all top 5 time preferences
            for idx in range(min(5, len(timePreferences[i]))):
                pref = timePreferences[i][idx]
                # Time slots in range 0 to 19 only
                if 0 <= pref < 20: 
                    self.add_connection(student_node, self.TIME_START + pref, 1)


    def build_class_flow(self, proposedClasses):
        """
        :Function description:
            Connects time slot nodes to corresponding class nodes with N capacity.

        :Input:
            proposedClasses (List[Tuple[int, int, int]]): Proposed classes with time_slot, minimum capacity and maximum capacity.

        :Time complexity:
            O(M), where M is the number of classes.

        :Time complexity analysis:
            Linear time for connecting each time slot node to corresponding class node.

        :Space complexity:
            O(1)

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

        """
        # Connect corresponding classes
        for i in range(self.classes):
            time_slot = proposedClasses[i][0]
            # Time slots in range 0 to 19 only
            if 0 <= time_slot < 20:
                self.add_connection(self.TIME_START + time_slot, self.CLASS_START + i, self.students)


    def build_alternative_flow(self, minimumSatisfaction):
        """
        :Function description:
            Adds alternative path for students to be placed in a class with not chosen or not allocated with time preference.

        :Input:
            minimumSatisfaction (int): Satisfaction number of students with allocated preferred time slots

        :Time complexity:
            O(N + M) --> O(N)
            where N is the number of students (dominating) and M is the number of classes.

        :Time complexity analysis:
            Linear time for connecting each student node to alternative nodes and then to class nodes.

        :Space complexity:
            O(1)

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

        """
        # Connect each student to alternative nodes
        for i in range(self.students):
            self.add_connection(self.STUDENT_START + i, self.ALTERNATIVE1, 1)
        # Connect alternative node to alternative node to filter students not chosen time preference
        self.add_connection(self.ALTERNATIVE1, self.ALTERNATIVE2, self.students - minimumSatisfaction)
        # Connect alternative node to each class node
        for i in range(self.classes):
            self.add_connection(self.ALTERNATIVE2, self.CLASS_START + i, self.students)


    def build_sink_flow(self, proposedClasses, sum_min_capacity):
        """
        :Function description:
            Connects each class to sink node and super sink node with minimum and maximum capacity constraints.

        :Input:
            proposedClasses (List[Tuple[int, int, int]]): Proposed classes with time_slot, minimum capacity and maximum capacity.
            sum_min_capacity (int): Sum of minimum capacities of all classes

        :Time complexity:
            O(M), where M is the number of students.

        :Time complexity analysis:
            Linear time for connecting each class node to sink and super sink nodes.

        :Space complexity:
            O(1)

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

        """
        # Connect each class to sink and super sink nodes
        for i in range(self.classes):
            class_node = self.CLASS_START + i
            min_capacity = proposedClasses[i][1]
            max_capacity = proposedClasses[i][2]
            self.add_connection(class_node, self.SUPER_SINK, min_capacity)
            self.add_connection(class_node, self.SINK, max_capacity - min_capacity)
        # Connect sink node to super sink node with remaining flow
        self.add_connection(self.SINK, self.SUPER_SINK, self.students - sum_min_capacity)

    def allocate(self):
        """
        :Function description:
            Performs allocation from the final flow result in AllocationNetwork.

        :Output:
            List[int] | None: Allocation list of students to class index or None if impossible

        :Time complexity:
            O(N * M), where N is the number of students and M is the number of classes.

        :Time complexity analysis:
            Linear time for scanning each student node connections, then scanning the time nodes 
            or class nodes for allocation, resulting in O(5N) or O(N * M) time complexity.

        :Space complexity:
            O(N), where N is the number of students.

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(N) for the storing of allocation.
            
        """
        # Final allocation of students to classes
        allocation = [None] * self.students

        # Check each student node connections
        for i in range(self.students):
            student_node = self.nodes[self.STUDENT_START + i]
            for connection in student_node.connections:
                # Valid allocation flow
                if (connection.flow > 0):
                    # CASE 1 !!! Satisfaction with allocated time preference! 
                    if (self.TIME_START <= connection.end < (self.TIME_START + 20)):
                        time_node = self.nodes[connection.end]
                        # Carry out allocation in time-class connections
                        for class_connection in time_node.connections:
                            if ((self.CLASS_START <= class_connection.end < (self.CLASS_START + self.classes)) and (class_connection.flow > 0)):
                                # Allocate class now
                                allocation[i] = class_connection.end - self.CLASS_START
                                # Not use this flow again
                                class_connection.flow -= 1
                                break
                    # CASE 2 !!! Satisfaction with no time preference! With intermediate path!
                    elif connection.end == self.ALTERNATIVE1:
                        alternative_node = self.nodes[self.ALTERNATIVE2]
                        # Carry out allocation in alternative-class connections
                        for class_connection in alternative_node.connections:
                            if ((self.CLASS_START <= class_connection.end < (self.CLASS_START + self.classes)) and (class_connection.flow > 0)):
                                # Allocate class now
                                allocation[i] = class_connection.end - self.CLASS_START
                                # Not use this flow again
                                class_connection.flow -= 1
                                break

        # CASE 3 !!! No satisfaction!
        if None in allocation:
            return None
        else:
            return allocation
        


class AllocationFlow:
    """
    This class represents a flow edge in the AllocationNetwork, a possible assignment to a decision point
    that consists of a start node, end node, capacity, current flow and reverse edge (for residual tracking).
    """

    def __init__(self, start, end, capacity):
        """
        :Function description:
            AllocationFlow constructor for constructing a flow connection between two nodes in the AllocationNetwork.
            
        :Input:
            start    (int) : Starting node identification number
            end      (int) : Ending node identification number
            capacity (int) : Maximum flow capacity
            
        :Time complexity:
            O(1)

        :Time complexity analysis:
            Constant time for initialisation of the flow edge attributes.
            
        :Space complexity:
            O(1)
        
        :Space complexity analysis:
            Constant space for input and auxiliary.

        """
        # Start and end of allocation flow
        self.start = start
        self.end = end
        # Maximum flow capacity
        self.capacity = capacity
        # Current flow and reverse direction flow
        self.flow = 0
        self.reverse = None



class AllocationPoint:
    """
    This class represents a node in the AllocationNetwork, a decision point in the allocation process the contains 
    information on the node identification number, a discovery flag (for BFS implementation), incoming flow edge and list of connections.
    """

    def __init__(self, node_no):
        """
        :Function description:
            AllocationPoint constructor for constructing a node in the AllocationNetwork.

        :Input:
            node_no (int): Node identification number.

        :Time complexity:
            O(1)

        :Time complexity analysis:
            Constant time for initialisation of the node attributes.

        :Space complexity:
            O(N), where N is the number of students (nodes).
        
        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(N) for the storing of connections in the node (students dominate).
        
        """
        self.node_no = node_no
        self.discovered = False
        # Incoming edge to this node
        self.incoming_connection = None
        # List of connections from node to nodes
        self.connections = []


    def connect(self, connection):
        """
        :Function description:
            Add outgoing connection to this node.

        :Input:
            connection (AllocationFlow): Connection to add.

        :Time complexity:
            O(1)

        :Time complexity analysis:
            Amortised complexity for append().

        :Space complexity:
            O(N), where N is the number of students.

        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(N).
            Since N >= M, where N is the number of student connections and M is the number of class connections, 
            N dominates the space complexity and other constant connections do not affect the space complexity.
            Thus, the space complexity simplifies to O(N).

        """
        self.connections.append(connection)



def crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction):
    """
    :Function description:
        Main function to construct the entire allocation network and obtain a feasible allocation.

    :Input:
        n                   (int)           : Number of students.
        m                   (int)           : Number of classes.
        timePreferences (List[List[int]])   : Preferences of students (up to 5 time slots).
        proposedClasses (List[Tuple[int, int, int]]): Each class with its time slot, minimum capacity and maximum capacity.
        minimumSatisfaction (int)           : Satisfaction number of students to be allocated with preferred time.

    :Output:
        List[int] | None: Allocation list of students to class index or None if impossible

    :Time complexity:
        O(N^2), where N is the number of students.

    :Time complexity analysis:
        - O(M) for calculating total minimum capacity of classes for logical check.
        - O(N) for constructing the AllocationNetwork.
        - O(N) for building student flow connections.
        - O(N) for building time flow connections.
        - O(M) for building class flow connections.
        - O(N) for building alternative flow connections.
        - O(M) for building sink flow connections.
        - O(N^2) for running Ford-Fulkerson algorithm with BFS.
        - O(N*M) for carrying out allocation.
        Accurately, the time complexity is O(3M + 4N + N^2 + NM).
        Since N dominates M as the number of students must be more than or equals to the number of classes, N dominates the time complexity.
        Hence, the overall time complexity is dominated by the performance of Ford-Fulkerson algorithm, resulting in O(N^2).

    :Space complexity:
        O(N), where N is the number of students.

    :Space complexity analysis:
        Input space of O(1), and auxiliary space of O(N) for allocation list.

    """
    total_min_capacity = 0
    for c in proposedClasses:
        total_min_capacity += c[1]  

    # Total minimum capcity of all classes must meet the number of students
    if total_min_capacity <= n:

        # Construction of the AllocationNetwork
        network = AllocationNetwork(n, m)
        network.build_student_flow()
        network.build_time_flow(timePreferences)
        network.build_class_flow(proposedClasses)
        network.build_alternative_flow(minimumSatisfaction)
        network.build_sink_flow(proposedClasses, total_min_capacity)

        # Maximum flow computation
        if network.run_ford_fulkerson() != n: 
            return None
        else: 
            # Allocation of students to classes
            return network.allocate()
    else:
        return None




"""
===========================================================================================================

**** TASK 2 - Typo ****

:Module description:
This module is a program for user to identify input words that have exactly 
one character substitution (Levenshtein distance of one) from the words in a
given dictionary. A Trie-based solution is implemented to efficiently store all 
dictionary words and optimise search process efficient lookup time by the Trie data structure.

:Classes:
TrieNode    : A single Trie node that contains a complete word and character links.
Bad_AI      : A Trie for efficient searching of words with one character substitution from the given dictionary. 

===========================================================================================================
"""

__author__ = "Er Jun Yet"


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
        root        (TrieNode)  : Root node of the Trie data structure.
        
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
        self.root = TrieNode()
        # Each word of each char in the Trie
        for word in list_words:
            self.add_word(word)
    

    def get_index(self, char):
        """
        :Function description:
            Get the corresponding character index in the links array of TrieNode.

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
            Linear time for inserting each character TrieNode of the word into the Trie.

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
                current_node.links[index] = TrieNode()
                current_node = self.next_char(current_node, index)
            else:
                current_node = self.next_char(current_node, index)

        # Store complete word at the terminal node
        word_index = self.get_index('$')
        if current_node.get_word() is None:
            current_node.links[word_index] = TrieNode()
            current_node.links[word_index].word = word
        else:
            current_node.links[word_index].word = word


    def next_char(self, current_node, current_index):
        """
        :Function description:
            Traverse to next Node in Trie with links array.

        :Input:
            current_node (TrieNode): Current node.
            current_index (int): Character index in links array.

        :Output:
            TrieNode or None: The next node or None (no next node).

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
        # Trie node index same as char substitution index
        if node_index == sus_index: 
            current_char = new_char # Successful char substitution
            current_index = self.get_index(current_char)
        else: 
            current_char = sus_word[node_index] # Original character remains
            current_index = self.get_index(current_char)
        return current_index, current_char
    

    def check_word(self, sus_word):
        """
        :Function description:
            Examine a suspicious word for possible word by one character substitution.

        :Input:
            sus_word (str): Suspicious word to check.
        
        :Output:
            results (list): List of words with one character away from suspicious word.
        
        :Time complexity:
            O(J*N), where J is the number of characters in suspicious word and N is the number of words in the Trie.
        
        :Time complexity analysis:
            - O(J) for checking each character position in the suspicious word.
            - O(26) for attempting character substitution for all alphabets.
            - O(N) for checking each character in the Trie dictionary.
              Not considered to be O(J) as it is not bounded by J but by N, the number of words in the Trie.
              Since a Trie-based pruning is introduced by running through N valid words only, where only word exists
              in the Trie dictionary is checked, which means only viable nodes are checked, else early termination is introduced.
            Thus, the overall time complexity is O(J*N).

        :Space complexity:
            O(X), where X is the number of characters in result list.
        
        :Space complexity analysis:
            Input space of O(J) for the number of characters in suspicious word and auxiliary space 
            of O(X) for the number of characters in words in results list.

        """
        results = []
        sus_size = len(sus_word)
        trie_depth = len(sus_word)
        
        # Check each character in this suspicious word
        for sus_index in range(sus_size):
            original_char = sus_word[sus_index]
            
            # Attempt character substitution with all alphabets
            for new_char in self.ALPHABETS:

                # Same character, no substitution!!!
                if new_char != original_char:
                    current_node = self.root
                    match = True

                    # Check each character in the trie
                    for node_index in range(trie_depth):

                        # Character substitution or original character
                        current_index, current_char = self.replace_char(sus_word, node_index, sus_index, new_char)

                        # Check character exists in trie dictionary
                        if self.next_char(current_node, current_index) is not None:
                            current_node = self.next_char(current_node, current_index)                    
                        else: # Character not found in trie dictionary
                            match = False
                            current_node = self.next_char(current_node, current_index)  
                            break                  

                    # Arrive end of trie dictionary and obtain the complete word
                    if match == True:
                        if (current_node.get_word() is not None):
                            results.append(current_node.get_word())        
        return results



class TrieNode:
    """
    This class represents a single node in a Trie data structure.
    """

    def __init__(self):
        """
        :Function description:
            A TrieNode constructor with 27 character links and a complete word stored (if it is an end node).

        :Time complexity:
            O(1)

        :Time complexity analysis:
            Constant time for initialisation of TrieNode attributes.
        
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
            str | None: The complete word stored at the terminal node or None (not a word).

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