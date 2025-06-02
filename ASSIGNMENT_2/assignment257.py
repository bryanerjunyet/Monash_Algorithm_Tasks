import queue

"""

**** TASK 1 - A Crowded Campus ****

:Module description (Part 1):
This module section is a program for campus to allocate students to classes based on their time preferences 
and campus class capacity constraints. A Flow-Network-based approach is used to model the allocation process
to ensure the best minimum satisfaction of students while adhering to the following constraints:
1. Each student is allocated to exactly one class.
2. Each class meets its minimum and maximum capacity requirements.
3. A minimum satisfaction number of students get one of their top 5 preferred time slots.

:Classes:
AllocationFlow    : A flow edge in the allocation network.
AllocationNode    : A node in the allocation network.
AllocationNetwork : A manager class for allocation network construction and flow processing.

"""

__author__ = "Er Jun Yet"


class AllocationNetwork:
    """
    :Class description:
        This is the main class of the program that is a manager class for construction of allocation network
        and processing of allocation flow through the network that models with a maximum flow with the Ford-Fulkerson algorithm.

    :Approach description:
        The purpose of such allocation Flow Network allows for best and efficient allocation of students to classes 
        based on their time preferences and class capacity constraints with the Ford-Fulkerson algorithm for maximum total students.

        The allocation network is designed with careful consideration with the following nodes and edges:
        - A source node connects to each student nodes.
        - Each student nodes connect to 5 preferred time nodes.
        - Each time nodes connect corresponding class nodes. 
        - Each student nodes also connect to an alternative node for alternative allocation without time preference.
        - Each class nodes connect to a super sink node with minimum flow to achieve minimum class capacity.
        - Each class nodes also connect to a sink node with remaining flow to achieve remaining class capacity.

    """
    def __init__(self, students, classes):
        """
        :Function description:
            AllocationNetwork constructor.
            
        :Input:
            start    (int) : Starting node ID
            end      (int) : Ending node ID
            capacity (int) : Maximum flow capacity
            
        :Time complexity:
            O(1)    
            
        :Space complexity:
            O(1)
            
        """
        self.SOURCE = 0
        self.STUDENT_START = 1
        self.TIME_START = self.STUDENT_START + students
        self.CLASS_START = self.TIME_START + 20
        self.ALTERNATIVE1 = self.CLASS_START + classes
        self.ALTERNATIVE2 = self.ALTERNATIVE1 + 1
        self.SINK = self.ALTERNATIVE2 + 1
        self.SUPER_SINK = self.SINK + 1
        self.TOTAL_VERTICES = self.SUPER_SINK + 1

        self.students = students
        self.classes = classes
        self.vertices = []
        for i in range(self.TOTAL_VERTICES):
            self.vertices.append(AllocationNode(i))

    def connect(self, start, end, capacity):
        forward = AllocationFlow(start, end, capacity)
        backward = AllocationFlow(end, start, 0)
        forward.reverse = backward
        backward.reverse = forward
        self.vertices[start].connect(forward)
        self.vertices[end].connect(backward)
        return forward
    
    def reset(self):
        """
        Helper function to reset the discovered and incoming_connection attributes
        of all nodes in the network before running BFS.
        """
        for node in self.vertices:
            node.discovered = False
            node.incoming_connection = None

    def bfs(self):
        self.reset()

        path = queue.Queue()
        source_node = self.vertices[self.SOURCE]
        source_node.discovered = True
        path.put(source_node)

        while not path.empty():
            start = path.get()
            if start.id == self.SUPER_SINK:
                return True
            for connection in start.connections:
                residual = connection.capacity - connection.flow
                if residual > 0:
                    end = self.vertices[connection.end]
                    if not end.discovered:
                        end.discovered = True
                        end.incoming_connection = connection
                        path.put(end)
        return False

    def ford_fulkerson(self):
        max_flow = 0
        while self.bfs():
            path_flow = float('inf')
            v = self.vertices[self.SUPER_SINK]
            while v.id != self.SOURCE:
                connection = v.incoming_connection
                path_flow = min(path_flow, connection.capacity - connection.flow)
                v = self.vertices[connection.start]

            v = self.vertices[self.SUPER_SINK]
            while v.id != self.SOURCE:
                connection = v.incoming_connection
                connection.flow += path_flow
                connection.reverse.flow -= path_flow
                v = self.vertices[connection.start]

            max_flow += path_flow
        return max_flow

    def build_student_flow(self):
        for i in range(self.students):
            self.connect(self.SOURCE, self.STUDENT_START + i, 1)

    def build_time_flow(self, timePreferences):
        for i in range(self.students):
            student_node = self.STUDENT_START + i
            for idx in range(min(5, len(timePreferences[i]))):
                pref = timePreferences[i][idx]
                if 0 <= pref < 20:
                    self.connect(student_node, self.TIME_START + pref, 1)

    def build_class_flow(self, proposedClasses):
        for j in range(self.classes):
            time_slot = proposedClasses[j][0]
            if 0 <= time_slot < 20:
                self.connect(self.TIME_START + time_slot, self.CLASS_START + j, self.students)

    def build_intermediate_flow(self, minimumSatisfaction):
        for i in range(self.students):
            self.connect(self.STUDENT_START + i, self.ALTERNATIVE1, 1)
        self.connect(self.ALTERNATIVE1, self.ALTERNATIVE2, self.students - minimumSatisfaction)
        for j in range(self.classes):
            self.connect(self.ALTERNATIVE2, self.CLASS_START + j, self.students)

    def build_sink_flow(self, proposedClasses, total_min):
        for j in range(self.classes):
            class_node = self.CLASS_START + j
            min_cap, max_cap = proposedClasses[j][1], proposedClasses[j][2]
            self.connect(class_node, self.SUPER_SINK, min_cap)
            self.connect(class_node, self.SINK, max_cap - min_cap)
        self.connect(self.SINK, self.SUPER_SINK, self.students - total_min)

    def allocate(self):
        allocation = [None] * self.students
        for i in range(self.students):
            student_node = self.vertices[self.STUDENT_START + i]
            for connection in student_node.connections:
                if connection.flow > 0:
                    if self.TIME_START <= connection.end < self.TIME_START + 20:
                        for connection2 in self.vertices[connection.end].connections:
                            if self.CLASS_START <= connection2.end < self.CLASS_START + self.classes and connection2.flow > 0:
                                allocation[i] = connection2.end - self.CLASS_START
                                connection2.flow -= 1
                                break
                    elif connection.end == self.ALTERNATIVE1:
                        for connection2 in self.vertices[self.ALTERNATIVE2].connections:
                            if self.CLASS_START <= connection2.end < self.CLASS_START + self.classes and connection2.flow > 0:
                                allocation[i] = connection2.end - self.CLASS_START
                                connection2.flow -= 1
                                break

        if None not in allocation:
            return allocation
        else:
            return None
        


class AllocationFlow:
    """
    This class represents a flow edge in the allocation network graph.
    
    :Class description:
        Each edge maintains information about its capacity, current flow, and reverse edge
        for implementing the Ford-Fulkerson algorithm.
        
    :Attributes:
        start    (int) : Starting node ID of the edge
        end      (int) : Ending node ID of the edge
        capacity (int) : Maximum flow capacity of the edge
        flow     (int) : Current flow through the edge
        reverse (AllocationFlow) : Corresponding reverse edge for residual graph
    """
    def __init__(self, start, end, capacity):
        """
        :Function description:
            Allocation Flow constructor for constructing a flow connection 
            between two nodes in the allocation network.
            
        :Input:
            start    (int) : Starting node ID number
            end      (int) : Ending node ID number
            capacity (int) : Maximum flow capacity
            
        :Time complexity:
            O(1)
            
        :Space complexity:
            O(1)

        """
        # Start and end of allocation flow (AllocationNode IDs)
        self.start = start
        self.end = end
        # Maximum flow capacity
        self.capacity = capacity
        # Current flow and reverse direction flow
        self.flow = 0
        self.reverse = None



class AllocationNode:
    def __init__(self, id):
        self.id = id
        self.discovered = False
        self.incoming_connection = None
        self.connections = []

    def connect(self, connection):
        self.connections.append(connection)



def crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction):
    """
    :Function description:
        Constructs and solves the Crowded Campus student allocation problem using maximum flow.

    :Approach description:
        - Uses the AllocationNetwork class to build a custom flow network from the input.
        - Runs the Ford-Fulkerson algorithm via the NetworkFlow class to compute max flow.
        - Extracts the list of allocated student-class pairs from the final flow.

    :Time complexity:
        O(nm^2)

    :Time complexity analysis:
        - Graph construction takes O(n^2 + nm)
        - Ford-Fulkerson behaves as O(nm^2) in sparse graphs
        - Extraction takes O(nm)

    :Space complexity:
        O(nm)

    :Space complexity analysis:
        Space used to store the adjacency list, flow matrices and allocation results.
    """
    total_min = 0
    for c in proposedClasses:
        total_min += c[1]  
    if total_min > n:
        return None

    network = AllocationNetwork(n, m)
    network.build_student_flow()
    network.build_time_flow(timePreferences)
    network.build_class_flow(proposedClasses)
    network.build_intermediate_flow(minimumSatisfaction)
    network.build_sink_flow(proposedClasses, total_min)

    if network.ford_fulkerson() != n:
        return None
    else:
        return network.allocate()
