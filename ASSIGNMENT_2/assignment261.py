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
    Greedy approach: maximize satisfaction, then fill to meet min/max.
    """
    if n == 0 or m == 0:
        return None if n > 0 else []

    # Track assignments and class loads
    allocation = [-1] * n
    class_load = [0] * m
    satisfied = 0

    # Phase 1: Assign students to their top 5 preferred classes if possible
    for student in range(n):
        assigned = False
        for k in range(min(5, len(timePreferences[student]))):
            time_slot = timePreferences[student][k]
            for class_id in range(m):
                if (proposedClasses[class_id][0] == time_slot and
                    class_load[class_id] < proposedClasses[class_id][2]):
                    allocation[student] = class_id
                    class_load[class_id] += 1
                    satisfied += 1
                    assigned = True
                    break
            if assigned:
                break

    # Phase 2: Assign unassigned students to any class with available capacity
    for student in range(n):
        if allocation[student] == -1:
            for k in range(len(timePreferences[student])):
                time_slot = timePreferences[student][k]
                for class_id in range(m):
                    if (proposedClasses[class_id][0] == time_slot and
                        class_load[class_id] < proposedClasses[class_id][2]):
                        allocation[student] = class_id
                        class_load[class_id] += 1
                        break
                if allocation[student] != -1:
                    break

    # Check if all students are assigned
    if any(a == -1 for a in allocation):
        return None

    # Check class min constraints
    for class_id in range(m):
        if class_load[class_id] < proposedClasses[class_id][1]:
            # Try to reassign students from overfilled classes to this class
            needed = proposedClasses[class_id][1] - class_load[class_id]
            for student in range(n):
                if allocation[student] != class_id:
                    # Can this student be moved?
                    old_class = allocation[student]
                    if (proposedClasses[class_id][0] in timePreferences[student] and
                        class_load[old_class] > proposedClasses[old_class][1]):
                        allocation[student] = class_id
                        class_load[class_id] += 1
                        class_load[old_class] -= 1
                        needed -= 1
                        if needed == 0:
                            break
            if class_load[class_id] < proposedClasses[class_id][1]:
                return None

    # Recompute satisfaction
    satisfied = 0
    for student in range(n):
        class_id = allocation[student]
        time_slot = proposedClasses[class_id][0]
        for k in range(min(5, len(timePreferences[student]))):
            if timePreferences[student][k] == time_slot:
                satisfied += 1
                break

    if satisfied < minimumSatisfaction:
        return None

    return allocation