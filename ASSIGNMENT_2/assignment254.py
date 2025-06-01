import queue

class Edge:
    """
    Represents an edge in the flow network with capacity and flow attributes.
    """
    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

class Vertex:
    """
    Represents a vertex in the flow network with edges and discovery status.
    """
    def __init__(self, id):
        self.id = id
        self.edges = []
        self.discovered = False
        self.incoming_edge = None

class FlowNetwork:
    """
    Represents a flow network with vertices and edges, capable of computing max flow.
    """
    def __init__(self, vertices_count):
        self.vertices = [Vertex(i) for i in range(vertices_count)]
        self.source_id = 0
        self.sink_id = vertices_count - 1

    def add_edge(self, u, v, capacity):
        """
        Adds a directed edge from u to v with given capacity.
        """
        edge = Edge(u, v, capacity)
        self.vertices[u].edges.append(edge)
        return edge

    def bfs(self):
        """
        Breadth-first search to find an augmenting path from source to sink.
        Returns True if path exists, False otherwise.
        """
        for vertex in self.vertices:
            vertex.discovered = False
            vertex.incoming_edge = None
        
        q = queue.Queue()
        q.put(self.vertices[self.source_id])
        self.vertices[self.source_id].discovered = True
        
        while not q.empty():
            u = q.get()
            if u.id == self.sink_id:
                return True
                
            for edge in u.edges:
                if edge.flow < edge.capacity:
                    v = self.vertices[edge.v]
                    if not v.discovered:
                        v.discovered = True
                        v.incoming_edge = edge
                        q.put(v)
        return False

    def ford_fulkerson(self):
        """
        Computes the max flow using the Ford-Fulkerson method with BFS.
        Returns the max flow value.
        """
        max_flow = 0
        while self.bfs():
            path_flow = float('inf')
            v = self.vertices[self.sink_id]
            
            # Find the minimum residual capacity along the path
            while v.id != self.source_id:
                edge = v.incoming_edge
                path_flow = min(path_flow, edge.capacity - edge.flow)
                v = self.vertices[edge.u]
                
            # Update flow along the path
            v = self.vertices[self.sink_id]
            while v.id != self.source_id:
                edge = v.incoming_edge
                edge.flow += path_flow
                
                # Update reverse edge (if it exists)
                found = False
                for rev_edge in self.vertices[edge.v].edges:
                    if rev_edge.v == edge.u:
                        rev_edge.flow -= path_flow
                        found = True
                        break
                if not found:
                    # Add reverse edge if it doesn't exist
                    rev_edge = Edge(edge.v, edge.u, 0)
                    rev_edge.flow = -path_flow
                    self.vertices[edge.v].edges.append(rev_edge)
                    
                v = self.vertices[edge.u]
                
            max_flow += path_flow
        return max_flow

def crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction):
    """
    Allocates students to classes while satisfying capacity constraints and minimum satisfaction requirements.
    Uses a flow network approach with Ford-Fulkerson algorithm to find a valid allocation.
    """
    # Calculate total min and max capacities
    total_min = sum(c[1] for c in proposedClasses)
    total_max = sum(c[2] for c in proposedClasses)
    
    # Early exit if total min > n or total max < n
    if total_min > n or total_max < n:
        return None
    
    # Vertex indices mapping
    SOURCE = 0
    STUDENT_START = 1
    TIME_PREF_START = STUDENT_START + n
    CLASS_START = TIME_PREF_START + 20  # 20 time slots
    INTERMEDIATE1 = CLASS_START + m
    INTERMEDIATE2 = INTERMEDIATE1 + 1
    SINK = INTERMEDIATE2 + 1
    SUPER_SINK = SINK + 1
    TOTAL_VERTICES = SUPER_SINK + 1
    
    # Create flow network
    network = FlowNetwork(TOTAL_VERTICES)
    
    # Connect source to students (capacity 1)
    for i in range(n):
        network.add_edge(SOURCE, STUDENT_START + i, 1)
    
    # Connect students to their top 5 time preferences
    for i in range(n):
        student_node = STUDENT_START + i
        for pref in timePreferences[i][:5]:
            if 0 <= pref < 20:  # Validate time slot
                time_node = TIME_PREF_START + pref
                network.add_edge(student_node, time_node, 1)
    
    # Map time slots to classes
    time_to_classes = [[] for _ in range(20)]
    for j in range(m):
        time_slot = proposedClasses[j][0]
        if 0 <= time_slot < 20:  # Validate time slot
            time_to_classes[time_slot].append(j)
    
    # Connect time preferences to corresponding classes
    for time_slot in range(20):
        time_node = TIME_PREF_START + time_slot
        for class_idx in time_to_classes[time_slot]:
            class_node = CLASS_START + class_idx
            network.add_edge(time_node, class_node, n)  # Large capacity
    
    # Connect students to intermediate nodes (for non-preferred allocations)
    for i in range(n):
        student_node = STUDENT_START + i
        network.add_edge(student_node, INTERMEDIATE1, 1)
    
    # Connect intermediate nodes with capacity restriction
    network.add_edge(INTERMEDIATE1, INTERMEDIATE2, n - minimumSatisfaction)
    
    # Connect intermediate node to all classes
    for j in range(m):
        class_node = CLASS_START + j
        network.add_edge(INTERMEDIATE2, class_node, n)  # Large capacity
    
    # Connect classes to sink and super sink
    for j in range(m):
        class_node = CLASS_START + j
        min_cap, max_cap = proposedClasses[j][1], proposedClasses[j][2]
        # Connect to super sink for minimum capacity
        network.add_edge(class_node, SUPER_SINK, min_cap)
        # Connect to regular sink for remaining capacity
        network.add_edge(class_node, SINK, max_cap - min_cap)
    
    # Connect sink to super sink
    network.add_edge(SINK, SUPER_SINK, n - total_min)
    
    # Compute max flow
    max_flow = network.ford_fulkerson()
    
    # Check if all students are allocated (flow == n)
    if max_flow != n:
        return None
    
    # Extract allocation
    allocation = [None] * n
    
    # Track class assignments
    class_counts = [0] * m
    
    # First pass: Assign students who got their preferred time slots
    for i in range(n):
        student_node = network.vertices[STUDENT_START + i]
        for edge in student_node.edges:
            if edge.flow > 0 and TIME_PREF_START <= edge.v < TIME_PREF_START + 20:
                time_slot = edge.v - TIME_PREF_START
                # Assign to first available class for this time slot
                for class_idx in time_to_classes[time_slot]:
                    if class_counts[class_idx] < proposedClasses[class_idx][2]:
                        allocation[i] = class_idx
                        class_counts[class_idx] += 1
                        edge.flow -= 1
                        break
                if allocation[i] is not None:
                    break
    
    # Second pass: Assign remaining students through intermediate path
    for i in range(n):
        if allocation[i] is None:
            student_node = network.vertices[STUDENT_START + i]
            for edge in student_node.edges:
                if edge.flow > 0 and edge.v == INTERMEDIATE1:
                    # Assign to first available class
                    for j in range(m):
                        if class_counts[j] < proposedClasses[j][2]:
                            allocation[i] = j
                            class_counts[j] += 1
                            edge.flow -= 1
                            break
                    break
    
    return allocation