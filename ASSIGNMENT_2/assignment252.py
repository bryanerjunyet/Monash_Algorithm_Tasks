from queue import Queue

class Vertex:
    def __init__(self, id: int):
        self.id = id
        self.edges = []
        self.visited = False
        self.incoming_edge = None

    def add_edge(self, edge):
        self.edges.append(edge)

class Edge:
    def __init__(self, u: int, v: int, capacity: int):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0
        self.reverse_edge = None

class FlowNetwork:
    def __init__(self, size: int, source: int, sink: int):
        self.vertices = [Vertex(i) for i in range(size)]
        self.source = source
        self.sink = sink
        self.size = size

    def add_edge(self, u: int, v: int, capacity: int):
        forward_edge = Edge(u, v, capacity)
        backward_edge = Edge(v, u, 0)
        forward_edge.reverse_edge = backward_edge
        backward_edge.reverse_edge = forward_edge
        self.vertices[u].add_edge(forward_edge)
        self.vertices[v].add_edge(backward_edge)

    def reset_vertices(self):
        for vertex in self.vertices:
            vertex.visited = False
            vertex.incoming_edge = None

    def bfs(self):
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
        max_flow = 0
        
        while self.bfs():
            path_flow = float('inf')
            v = self.sink
            
            while v != self.source:
                edge = self.vertices[v].incoming_edge
                path_flow = min(path_flow, edge.capacity - edge.flow)
                v = edge.u

            v = self.sink
            while v != self.source:
                edge = self.vertices[v].incoming_edge
                edge.flow += path_flow
                edge.reverse_edge.flow -= path_flow
                v = edge.u

            max_flow += path_flow

        return max_flow

def crowdedCampus(n: int, m: int, timePreferences: list, proposedClasses: list, minimumSatisfaction: int):
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
    
    # Create mapping from time slots to classes (only valid time slots 0-19)
    time_to_classes = [[] for _ in range(20)]
    for class_id, (time_slot, _, _) in enumerate(proposedClasses):
        if 0 <= time_slot < 20:
            time_to_classes[time_slot].append(class_id)
    
    # Create the flow network
    # Vertices: source (0), students (1..n), classes (n+1..n+m), sink (n+m+1)
    source = 0
    sink = n + m + 1
    network = FlowNetwork(sink + 1, source, sink)
    
    # Step 1: Connect source to students (capacity 1)
    for student in range(1, n+1):
        network.add_edge(source, student, 1)
    
    # Step 2: Connect students to classes they can attend based on preferences
    for student in range(n):
        student_node = student + 1
        top5 = timePreferences[student][:5]
        other = timePreferences[student][5:]
        
        # Connect to classes in top 5 preferences first
        for time in top5:
            for class_id in time_to_classes[time]:
                class_node = n + 1 + class_id
                network.add_edge(student_node, class_node, 1)
        
        # Then connect to other classes
        for time in other:
            for class_id in time_to_classes[time]:
                class_node = n + 1 + class_id
                network.add_edge(student_node, class_node, 1)
    
    # Step 3: Connect classes to sink with min/max capacities
    for class_id in range(m):
        class_node = n + 1 + class_id
        _, min_cap, max_cap = proposedClasses[class_id]
        
        # Add edge with max capacity
        network.add_edge(class_node, sink, max_cap)
        
        # To enforce min capacity, we need to ensure at least min_cap flow
        # We'll handle this by checking after running the flow
    
    # Run Ford-Fulkerson to get maximum flow
    max_flow = network.ford_fulkerson()
    
    # Check if all students are allocated
    if max_flow != n:
        return None
    
    # Check if class capacities are satisfied
    for class_id in range(m):
        class_node = n + 1 + class_id
        flow_to_class = 0
        for edge in network.vertices[class_node].edges:
            if edge.v == sink:
                flow_to_class = edge.flow
                break
        
        min_cap = proposedClasses[class_id][1]
        if flow_to_class < min_cap:
            return None
    
    # Check minimum satisfaction
    satisfied = 0
    allocation = [None] * n
    
    for class_id in range(m):
        class_node = n + 1 + class_id
        time_slot = proposedClasses[class_id][0]
        
        for edge in network.vertices[class_node].edges:
            if edge.v == sink:
                class_flow = edge.flow
                break
        
        # Find students in this class
        students_in_class = []
        for student in range(n):
            student_node = student + 1
            for edge in network.vertices[student_node].edges:
                if edge.v == class_node and edge.flow > 0:
                    students_in_class.append(student)
                    break
        
        # Assign students to this class
        for student in students_in_class:
            allocation[student] = class_id
            if time_slot in timePreferences[student][:5]:
                satisfied += 1
    
    if satisfied < minimumSatisfaction:
        return None
    
    return allocation