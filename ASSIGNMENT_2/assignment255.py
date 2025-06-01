import queue

class Edge:
    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0
        self.reverse = None

class Vertex:
    def __init__(self, id):
        self.id = id
        self.edges = []
        self.discovered = False
        self.incoming_edge = None

class FlowNetwork:
    def __init__(self, vertices_count):
        self.vertices = [Vertex(i) for i in range(vertices_count)]
        self.source_id = 0
        self.sink_id = vertices_count - 1

    def add_edge(self, u, v, capacity):
        forward = Edge(u, v, capacity)
        backward = Edge(v, u, 0)
        forward.reverse = backward
        backward.reverse = forward
        self.vertices[u].edges.append(forward)
        self.vertices[v].edges.append(backward)
        return forward

    def bfs(self):
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
        max_flow = 0
        while self.bfs():
            path_flow = float('inf')
            v = self.vertices[self.sink_id]
            while v.id != self.source_id:
                edge = v.incoming_edge
                path_flow = min(path_flow, edge.capacity - edge.flow)
                v = self.vertices[edge.u]
            v = self.vertices[self.sink_id]
            while v.id != self.source_id:
                edge = v.incoming_edge
                edge.flow += path_flow
                edge.reverse.flow -= path_flow
                v = self.vertices[edge.u]
            max_flow += path_flow
        return max_flow

def crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction):
    total_min = sum(c[1] for c in proposedClasses)
    total_max = sum(c[2] for c in proposedClasses)
    if total_min > n or total_max < n:
        return None

    SOURCE = 0
    STUDENT_START = 1
    TIME_PREF_START = STUDENT_START + n
    CLASS_START = TIME_PREF_START + 20
    INTERMEDIATE1 = CLASS_START + m
    INTERMEDIATE2 = INTERMEDIATE1 + 1
    SINK = INTERMEDIATE2 + 1
    SUPER_SINK = SINK + 1
    TOTAL_VERTICES = SUPER_SINK + 1

    network = FlowNetwork(TOTAL_VERTICES)

    for i in range(n):
        network.add_edge(SOURCE, STUDENT_START + i, 1)

    for i in range(n):
        student_node = STUDENT_START + i
        for pref in timePreferences[i][:5]:
            if 0 <= pref < 20:
                time_node = TIME_PREF_START + pref
                network.add_edge(student_node, time_node, 1)

    class_times = [c[0] for c in proposedClasses]

    for j in range(m):
        time_slot = class_times[j]
        if 0 <= time_slot < 20:
            time_node = TIME_PREF_START + time_slot
            class_node = CLASS_START + j
            network.add_edge(time_node, class_node, n)

    for i in range(n):
        student_node = STUDENT_START + i
        network.add_edge(student_node, INTERMEDIATE1, 1)

    network.add_edge(INTERMEDIATE1, INTERMEDIATE2, n - minimumSatisfaction)

    for j in range(m):
        class_node = CLASS_START + j
        network.add_edge(INTERMEDIATE2, class_node, n)

    for j in range(m):
        class_node = CLASS_START + j
        min_cap, max_cap = proposedClasses[j][1], proposedClasses[j][2]
        network.add_edge(class_node, SUPER_SINK, min_cap)
        network.add_edge(class_node, SINK, max_cap - min_cap)

    network.add_edge(SINK, SUPER_SINK, n - total_min)

    max_flow = network.ford_fulkerson()
    if max_flow != n:
        return None

    allocation = [None] * n
    class_usage = [0] * m

    for i in range(n):
        student_node = network.vertices[STUDENT_START + i]
        found = False
        for edge in student_node.edges:
            if edge.flow > 0:
                # Case 1: Preferred path (student -> time -> class)
                if TIME_PREF_START <= edge.v < TIME_PREF_START + 20:
                    for edge2 in network.vertices[edge.v].edges:
                        if CLASS_START <= edge2.v < CLASS_START + m and edge2.flow > 0:
                            class_idx = edge2.v - CLASS_START
                            allocation[i] = class_idx
                            edge2.flow -= 1
                            edge2.reverse.flow += 1
                            class_usage[class_idx] += 1
                            found = True
                            break
                    if found:
                        break
                # Case 2: Intermediate path (student -> intermediate1 -> intermediate2 -> class)
                elif edge.v == INTERMEDIATE1:
                    for edge1 in network.vertices[INTERMEDIATE1].edges:
                        if edge1.v == INTERMEDIATE2 and edge1.flow > 0:
                            for edge2 in network.vertices[INTERMEDIATE2].edges:
                                if CLASS_START <= edge2.v < CLASS_START + m and edge2.flow > 0:
                                    class_idx = edge2.v - CLASS_START
                                    allocation[i] = class_idx
                                    edge2.flow -= 1
                                    edge2.reverse.flow += 1
                                    class_usage[class_idx] += 1
                                    found = True
                                    break
                        if found:
                            break
                if found:
                    break

    # Final check to ensure all class minimums are satisfied
    for j in range(m):
        if class_usage[j] < proposedClasses[j][1]:
            return None

    if None in allocation:
        return None

    return allocation
