class Vertex:
    """
    Vertex class represents a node in the flow network.
    Each vertex has an ID and maintains a list of edges.
    """
    def __init__(self, id: int):
        self.id = id
        self.edges = []
        self.discovered = False
        self.incoming_edge = None

    def add_edge(self, edge):
        """Add an edge to this vertex's adjacency list."""
        self.edges.append(edge)

    def is_discovered(self):
        """Mark this vertex as discovered."""
        self.discovered = True

class Edge:
    """
    Edge class represents a directed edge in the flow network.
    It stores capacity and flow information.
    """
    def __init__(self, u: int, v: int, capacity: int):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

    def __str__(self):
        return f"{self.u} --({self.flow}/{self.capacity})-> {self.v}"

class ResidualEdge:
    """
    ResidualEdge class represents an edge in the residual graph.
    It stores residual capacity and references to its counterpart.
    """
    def __init__(self, u: int, v: int, weight: int):
        self.u = u
        self.v = v
        self.weight = weight
        self.original_edge = None
        self.reverse_edge = None
        self.type = None  # 'forward' or 'backward'

class FlowNetwork:
    """
    FlowNetwork class represents the complete flow network with source and sink.
    It implements the Ford-Fulkerson algorithm using BFS for finding augmenting paths.
    """
    def __init__(self, vertices_count: int, source_id: int, sink_id: int):
        self.vertices = [Vertex(i) for i in range(vertices_count)]
        self.source_id = source_id
        self.sink_id = sink_id

    def add_edge(self, u: int, v: int, capacity: int):
        """Add a directed edge from u to v with given capacity."""
        edge = Edge(u, v, capacity)
        self.vertices[u].add_edge(edge)

    def get_edges(self):
        """Get all edges in the flow network."""
        edges = []
        for vertex in self.vertices:
            edges.extend(vertex.edges)
        return edges

    def bfs(self, residual_vertices):
        """
        Perform BFS on the residual graph to find an augmenting path.
        Returns True if a path exists from source to sink, False otherwise.
        """
        # Reset vertex states
        for vertex in residual_vertices:
            vertex.discovered = False
            vertex.incoming_edge = None

        # Initialize queue with source
        queue = []
        source = residual_vertices[self.source_id]
        source.discovered = True
        queue.append(source)

        while queue:
            u = queue.pop(0)
            if u.id == self.sink_id:
                return True  # Found path to sink

            for edge in u.edges:
                if edge.weight > 0:  # Only consider edges with residual capacity
                    v = residual_vertices[edge.v]
                    if not v.discovered:
                        v.discovered = True
                        v.incoming_edge = edge
                        queue.append(v)
        return False

    def ford_fulkerson(self):
        """
        Implement the Ford-Fulkerson algorithm using BFS (Edmonds-Karp).
        Returns the maximum flow value and updates the flow network.
        """
        # Create residual graph
        residual_vertices = [Vertex(i) for i in range(len(self.vertices))]
        
        # Add residual edges (forward and backward)
        for edge in self.get_edges():
            # Forward edge with residual capacity
            forward = ResidualEdge(edge.u, edge.v, edge.capacity - edge.flow)
            forward.type = 'forward'
            forward.original_edge = edge
            residual_vertices[edge.u].add_edge(forward)

            # Backward edge with residual capacity
            backward = ResidualEdge(edge.v, edge.u, edge.flow)
            backward.type = 'backward'
            backward.original_edge = edge
            residual_vertices[edge.v].add_edge(backward)

            # Link edges
            forward.reverse_edge = backward
            backward.reverse_edge = forward

        max_flow = 0
        while self.bfs(residual_vertices):
            # Find bottleneck capacity
            flow = float('inf')
            v = residual_vertices[self.sink_id]
            while v.id != self.source_id:
                edge = v.incoming_edge
                flow = min(flow, edge.weight)
                v = residual_vertices[edge.u]

            # Update flow along the path
            v = residual_vertices[self.sink_id]
            while v.id != self.source_id:
                edge = v.incoming_edge
                edge.weight -= flow
                edge.reverse_edge.weight += flow

                # Update original flow network
                if edge.type == 'forward':
                    edge.original_edge.flow += flow
                else:
                    edge.original_edge.flow -= flow

                v = residual_vertices[edge.u]

            max_flow += flow

        return max_flow

def crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction):
    """
    Function description:
    Allocates students to classes while satisfying capacity constraints and minimum satisfaction requirements.
    Uses a flow network approach with Ford-Fulkerson algorithm to find a valid allocation.

    Approach description:
    1. Construct a flow network with:
       - Source connected to students (capacity 1)
       - Students connected to classes they can attend (based on time preferences)
       - Classes connected to sink with capacity between min and max students
    2. Ensure at least 'minimumSatisfaction' students get their top 5 preferences by:
       - First trying to allocate these students to their preferred classes
       - Then allocating remaining students
    3. Use Ford-Fulkerson with BFS to find the maximum flow that satisfies all constraints

    :Input:
    n: Number of students
    m: Number of proposed classes
    timePreferences: List of time slot preferences for each student
    proposedClasses: List of proposed classes with time slot and capacity constraints
    minimumSatisfaction: Minimum number of students who must get top 5 preferences

    :Output, return or postcondition:
    Returns a list of class allocations for each student if a valid allocation exists,
    otherwise returns None.

    :Time complexity: O(n^2) - Dominated by Ford-Fulkerson on a network with O(n) vertices
    :Space complexity: O(n) - Flow network size scales linearly with number of students
    """
    # Special case: no students or no classes
    if n == 0 or m == 0:
        return None if n > 0 else []

    # Create flow network
    # Vertex IDs:
    # 0 to n-1: students
    # n to n+m-1: classes
    # n+m: source
    # n+m+1: sink
    source = n + m
    sink = n + m + 1
    total_vertices = n + m + 2
    network = FlowNetwork(total_vertices, source, sink)

    # Step 1: Connect source to students (capacity 1)
    for student in range(n):
        network.add_edge(source, student, 1)

    # Step 2: Connect classes to sink with min/max capacities
    # We need to ensure each class has between min and max students
    # To handle this, we'll use a standard flow network trick:
    # Split each class into two nodes with edges between them having min/max capacity
    for class_id in range(m):
        min_cap = proposedClasses[class_id][1]
        max_cap = proposedClasses[class_id][2]
        # Edge from class node to sink with capacity (max - min)
        network.add_edge(n + class_id, sink, max_cap - min_cap)
        # Edge from source to class node with capacity min (ensures at least min students)
        network.add_edge(source, n + class_id, min_cap)

    # Step 3: Connect students to classes they can attend
    # First pass: connect students to their top 5 preferred classes
    top5_edges = []
    for student in range(n):
        preferred_times = set(timePreferences[student][:5])
        for class_id in range(m):
            if proposedClasses[class_id][0] in preferred_times:
                top5_edges.append((student, n + class_id, 1))

    # Second pass: connect all other possible allocations
    other_edges = []
    for student in range(n):
        all_times = set(timePreferences[student])
        for class_id in range(m):
            if proposedClasses[class_id][0] in all_times:
                other_edges.append((student, n + class_id, 1))

    # Add edges in order: top5 first, then others
    for u, v, capacity in top5_edges + other_edges:
        network.add_edge(u, v, capacity)

    # Calculate required flow (must be exactly n)
    required_flow = n

    # Run Ford-Fulkerson
    max_flow = network.ford_fulkerson()

    # Check if we achieved the required flow
    if max_flow != required_flow:
        return None

    # Extract allocation from flow network
    allocation = [None] * n
    for student in range(n):
        for edge in network.vertices[student].edges:
            if edge.flow > 0 and edge.v >= n and edge.v < n + m:
                allocation[student] = edge.v - n
                break

    # Verify minimum satisfaction constraint
    satisfied = 0
    for student in range(n):
        class_id = allocation[student]
        time_slot = proposedClasses[class_id][0]
        if time_slot in timePreferences[student][:5]:
            satisfied += 1

    if satisfied < minimumSatisfaction:
        return None

    return allocation