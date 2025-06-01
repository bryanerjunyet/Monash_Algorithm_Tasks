from queue import Queue

class Vertex:
    """
    Vertex class representing a node in the flow network
    """
    def __init__(self, id: int):
        self.id = id
        self.edges = []
        self.visited = False
        self.incoming_edge = None

    def add_edge(self, edge):
        self.edges.append(edge)

class Edge:
    """
    Edge class for the flow network
    """
    def __init__(self, u: int, v: int, capacity: int):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0
        self.reverse_edge = None

class FlowNetwork:
    """
    Flow network implementation for the student-class allocation problem
    """
    def __init__(self, size: int, source: int, sink: int):
        self.vertices = [Vertex(i) for i in range(size)]
        self.source = source
        self.sink = sink
        self.size = size

    def add_edge(self, u: int, v: int, capacity: int):
        """
        Add a directed edge from u to v with given capacity
        Also creates a reverse edge with 0 capacity
        """
        forward_edge = Edge(u, v, capacity)
        backward_edge = Edge(v, u, 0)
        forward_edge.reverse_edge = backward_edge
        backward_edge.reverse_edge = forward_edge
        
        self.vertices[u].add_edge(forward_edge)
        self.vertices[v].add_edge(backward_edge)

    def reset_vertices(self):
        """
        Reset all vertices' visited status and incoming edges
        """
        for vertex in self.vertices:
            vertex.visited = False
            vertex.incoming_edge = None

    def bfs(self):
        """
        Breadth-first search to find an augmenting path from source to sink
        Returns True if a path exists, False otherwise
        """
        self.reset_vertices()
        q = Queue()
        q.put(self.vertices[self.source])
        self.vertices[self.source].visited = True

        while not q.empty():
            current = q.get()
            
            if current.id == self.sink:
                return True

            for edge in current.edges:
                if edge.capacity > edge.flow and not self.vertices[edge.v].visited:
                    self.vertices[edge.v].visited = True
                    self.vertices[edge.v].incoming_edge = edge
                    q.put(self.vertices[edge.v])

        return False

    def ford_fulkerson(self):
        """
        Ford-Fulkerson algorithm to compute maximum flow
        Returns the maximum flow value
        """
        max_flow = 0
        
        while self.bfs():
            # Find the minimum residual capacity along the path
            path_flow = float('inf')
            v = self.sink
            
            while v != self.source:
                edge = self.vertices[v].incoming_edge
                path_flow = min(path_flow, edge.capacity - edge.flow)
                v = edge.u

            # Update flow along the path
            v = self.sink
            while v != self.source:
                edge = self.vertices[v].incoming_edge
                edge.flow += path_flow
                edge.reverse_edge.flow -= path_flow
                v = edge.u

            max_flow += path_flow

        return max_flow

def crowdedCampus(n: int, m: int, timePreferences: list, proposedClasses: list, minimumSatisfaction: int):
    """
    Allocates students to classes based on preferences and constraints
    
    Approach:
    1. Model the problem as a flow network with students, time slots, and classes
    2. First ensure minimum satisfaction by allocating students to top 5 preferences
    3. Then allocate remaining students to any available class
    4. Use Ford-Fulkerson to find a valid flow that meets all constraints
    
    :Input:
    n: number of students
    m: number of proposed classes
    timePreferences: list of time slot preferences for each student
    proposedClasses: list of proposed classes with time slot and capacity constraints
    minimumSatisfaction: minimum number of students who must get top 5 preferences
    
    :Output:
    A list of class allocations for each student, or None if no valid allocation exists
    
    :Time complexity: O(n^2)
    :Space complexity: O(n)
    """
    # Check trivial impossible cases
    if n == 0 or m == 0:
        return None
    
    # Check if total min capacity exceeds number of students
    total_min = sum(c[1] for c in proposedClasses)
    if total_min > n:
        return None
    
    # Check if total max capacity is less than number of students
    total_max = sum(c[2] for c in proposedClasses)
    if total_max < n:
        return None
    
    # Create mapping from time slots to classes
    time_to_classes = [[] for _ in range(20)]
    for class_id, (time_slot, _, _) in enumerate(proposedClasses):
        time_to_classes[time_slot].append(class_id)
    
    # Create the flow network
    # Vertices: source (0), students (1..n), time slots (n+1..n+20), classes (n+21..n+20+m), sink (n+21+m)
    source = 0
    sink = n + 21 + m
    network = FlowNetwork(sink + 1, source, sink)
    
    # Step 1: Connect source to students (capacity 1)
    for student in range(1, n+1):
        network.add_edge(source, student, 1)
    
    # Step 2: Connect students to their top 5 time slots (capacity 1)
    for student in range(n):
        student_node = student + 1
        top5 = timePreferences[student][:5]
        for time in top5:
            time_node = n + 1 + time
            network.add_edge(student_node, time_node, 1)
    
    # Step 3: Connect time slots to classes (capacity infinity)
    for time in range(20):
        time_node = n + 1 + time
        for class_id in time_to_classes[time]:
            class_node = n + 21 + class_id
            network.add_edge(time_node, class_node, float('inf'))
    
    # Step 4: Connect classes to sink with min/max capacities
    # We'll handle min capacity by forcing flow through those edges
    for class_id in range(m):
        class_node = n + 21 + class_id
        _, min_cap, max_cap = proposedClasses[class_id]
        network.add_edge(class_node, sink, max_cap)
    
    # First run: Ensure minimum satisfaction
    # We'll modify the network to prioritize top 5 preferences
    # Run Ford-Fulkerson to see if we can satisfy min_satisfaction
    flow = network.ford_fulkerson()
    
    # Check if we've allocated at least minimumSatisfaction students to top 5
    satisfied = 0
    for student in range(n):
        student_node = student + 1
        for edge in network.vertices[student_node].edges:
            if edge.flow > 0 and edge.v > n and edge.v <= n + 20:  # Connected to a time slot
                satisfied += 1
                break
    
    if satisfied < minimumSatisfaction:
        return None
    
    # Second run: Allocate remaining students
    # Connect all students to all time slots (not just top 5)
    for student in range(n):
        student_node = student + 1
        # Remove existing edges to time slots (only keep source edge)
        network.vertices[student_node].edges = [e for e in network.vertices[student_node].edges if e.u == source]
        
        # Add edges to all time slots
        for time in range(20):
            time_node = n + 1 + time
            network.add_edge(student_node, time_node, 1)
    
    # Reset flows
    for vertex in network.vertices:
        for edge in vertex.edges:
            edge.flow = 0
    
    # Run Ford-Fulkerson again to allocate all students
    total_flow = network.ford_fulkerson()
    
    if total_flow != n:
        return None
    
    # Extract the allocation
    allocation = [None] * n
    
    for class_id in range(m):
        class_node = n + 21 + class_id
        for edge in network.vertices[class_node].edges:
            if edge.v == sink:
                class_flow = edge.flow
                break
        
        # Find which students are in this class
        students_in_class = []
        time_node = None
        
        # Find the time slot feeding this class
        for time in range(20):
            time_node_candidate = n + 1 + time
            for edge in network.vertices[time_node_candidate].edges:
                if edge.v == class_node and edge.flow > 0:
                    time_node = time_node_candidate
                    break
            if time_node is not None:
                break
        
        if time_node is None:
            continue
        
        # Find students feeding this time slot
        for edge in network.vertices[time_node].edges:
            if edge.u >= 1 and edge.u <= n and edge.flow > 0:
                student_id = edge.u - 1
                allocation[student_id] = class_id
    
    # Verify all students are allocated
    if None in allocation:
        return None
    
    # Verify class capacities
    counts = [0] * m
    for a in allocation:
        counts[a] += 1
    for j in range(m):
        min_cap, max_cap = proposedClasses[j][1], proposedClasses[j][2]
        if not (min_cap <= counts[j] <= max_cap):
            return None
    
    # Verify minimum satisfaction
    satisfied = 0
    for i in range(n):
        class_id = allocation[i]
        time_slot = proposedClasses[class_id][0]
        if time_slot in timePreferences[i][:5]:
            satisfied += 1
    if satisfied < minimumSatisfaction:
        return None
    
    return allocation