class Vertex:
    """Represents a vertex in both original and residual graphs."""
    def __init__(self, id: int):
        self.id = id
        self.edges = []
        self.discovered = False
        self.incoming_edge = None

    def add_edge(self, edge):
        """Add an edge to this vertex's adjacency list."""
        self.edges.append(edge)

    def reset(self):
        """Reset vertex state for BFS."""
        self.discovered = False
        self.incoming_edge = None

class FlowEdge:
    """Represents an edge in the original flow network."""
    def __init__(self, u: int, v: int, capacity: int):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

    def residual_capacity(self):
        """Returns the remaining capacity that can be pushed."""
        return self.capacity - self.flow

class ResidualEdge:
    """Represents an edge in the residual graph."""
    def __init__(self, u: int, v: int, weight: int, original_edge=None, is_forward=True):
        self.u = u
        self.v = v
        self.weight = weight
        self.original_edge = original_edge
        self.is_forward = is_forward
        self.reverse_edge = None

class FlowNetwork:
    """Represents the complete flow network with source and sink."""
    def __init__(self, vertices_count: int, source_id: int, sink_id: int):
        self.vertices = [Vertex(i) for i in range(vertices_count)]
        self.source_id = source_id
        self.sink_id = sink_id
        self.edges = []

    def add_edge(self, u: int, v: int, capacity: int):
        """Add a directed edge from u to v with given capacity."""
        edge = FlowEdge(u, v, capacity)
        self.vertices[u].add_edge(edge)
        self.edges.append(edge)
        return edge

    def build_residual_graph(self):
        """Construct the residual graph from the current flow network."""
        residual_vertices = [Vertex(i) for i in range(len(self.vertices))]
        
        for edge in self.edges:
            # Forward edge with residual capacity
            if edge.residual_capacity() > 0:
                forward = ResidualEdge(edge.u, edge.v, edge.residual_capacity(), edge, True)
                residual_vertices[edge.u].add_edge(forward)
            
            # Backward edge with residual capacity
            if edge.flow > 0:
                backward = ResidualEdge(edge.v, edge.u, edge.flow, edge, False)
                residual_vertices[edge.v].add_edge(backward)
            
            # Link edges if they exist
            if edge.residual_capacity() > 0 and edge.flow > 0:
                forward.reverse_edge = backward
                backward.reverse_edge = forward
            
        return residual_vertices

    def bfs(self, residual_vertices):
        """Perform BFS on the residual graph to find an augmenting path."""
        for vertex in residual_vertices:
            vertex.reset()

        queue = [residual_vertices[self.source_id]]
        residual_vertices[self.source_id].discovered = True

        while queue:
            u = queue.pop(0)
            if u.id == self.sink_id:
                return True

            for edge in u.edges:
                if edge.weight > 0:
                    v = residual_vertices[edge.v]
                    if not v.discovered:
                        v.discovered = True
                        v.incoming_edge = edge
                        queue.append(v)
        return False

    def ford_fulkerson(self):
        """Implement the Ford-Fulkerson algorithm using BFS (Edmonds-Karp)."""
        max_flow = 0
        residual_vertices = self.build_residual_graph()

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
                if edge.reverse_edge:
                    edge.reverse_edge.weight += flow

                if edge.is_forward:
                    edge.original_edge.flow += flow
                else:
                    edge.original_edge.flow -= flow

                v = residual_vertices[edge.u]

            max_flow += flow
            residual_vertices = self.build_residual_graph()

        return max_flow

def crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction):
    """
    Allocates students to classes while satisfying constraints.
    Uses a flow network approach with Ford-Fulkerson algorithm.
    """
    if n == 0 or m == 0:
        return None if n > 0 else []

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

    # Step 2: Connect classes to sink with their exact capacities
    total_required = 0
    for class_id in range(m):
        _, min_cap, max_cap = proposedClasses[class_id]
        # For exact capacity requirements (min == max), we use max_cap
        capacity = max_cap
        total_required += capacity
        network.add_edge(n + class_id, sink, capacity)

    # Step 3: Connect students to classes they can attend
    # First pass: connect students to their top 5 preferred classes
    top_preferences = [set(student[:5]) for student in timePreferences]
    for student in range(n):
        for class_id in range(m):
            if proposedClasses[class_id][0] in top_preferences[student]:
                network.add_edge(student, n + class_id, 1)

    # Second pass: connect remaining possible allocations
    all_preferences = [set(student) for student in timePreferences]
    for student in range(n):
        for class_id in range(m):
            if (proposedClasses[class_id][0] in all_preferences[student] and 
                proposedClasses[class_id][0] not in top_preferences[student]):
                network.add_edge(student, n + class_id, 1)

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
            if isinstance(edge, FlowEdge) and edge.flow > 0 and n <= edge.v < n + m:
                allocation[student] = edge.v - n
                break
        else:
            return None

    # Verify class capacity constraints
    counts = [0] * m
    for a in allocation:
        counts[a] += 1
    for j in range(m):
        min_cap, max_cap = proposedClasses[j][1], proposedClasses[j][2]
        if not (min_cap <= counts[j] <= max_cap):
            return None

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