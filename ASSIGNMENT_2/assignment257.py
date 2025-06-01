import queue

class NetworkFlowEdge:
    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0
        self.reverse = None

class NetworkFlowNode:
    def __init__(self, id):
        self.id = id
        self.edges = []
        self.discovered = False
        self.incoming_edge = None

    def add_edge(self, edge):
        self.edges.append(edge)

class NetworkFlow:
    def __init__(self, node_count, source_id, sink_id):
        self.vertices = [NetworkFlowNode(i) for i in range(node_count)]
        self.source_id = source_id
        self.sink_id = sink_id

    def add_edge(self, u, v, capacity):
        forward = NetworkFlowEdge(u, v, capacity)
        backward = NetworkFlowEdge(v, u, 0)
        forward.reverse = backward
        backward.reverse = forward
        self.vertices[u].add_edge(forward)
        self.vertices[v].add_edge(backward)
        return forward

    def bfs(self):
        for node in self.vertices:
            node.discovered = False
            node.incoming_edge = None

        q = queue.Queue()
        source_node = self.vertices[self.source_id]
        source_node.discovered = True
        q.put(source_node)

        while not q.empty():
            u = q.get()
            if u.id == self.sink_id:
                return True
            for edge in u.edges:
                residual = edge.capacity - edge.flow
                if residual > 0:
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
    if total_min > n:
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

    network = NetworkFlow(TOTAL_VERTICES, SOURCE, SUPER_SINK)

    for i in range(n):
        network.add_edge(SOURCE, STUDENT_START + i, 1)

    for i in range(n):
        student_node = STUDENT_START + i
        for idx in range(min(5, len(timePreferences[i]))):
            pref = timePreferences[i][idx]
            if 0 <= pref < 20:
                network.add_edge(student_node, TIME_PREF_START + pref, 1)

    for j in range(m):
        time_slot = proposedClasses[j][0]
        if 0 <= time_slot < 20:
            network.add_edge(TIME_PREF_START + time_slot, CLASS_START + j, n)

    for i in range(n):
        network.add_edge(STUDENT_START + i, INTERMEDIATE1, 1)

    network.add_edge(INTERMEDIATE1, INTERMEDIATE2, n - minimumSatisfaction)

    for j in range(m):
        network.add_edge(INTERMEDIATE2, CLASS_START + j, n)

    for j in range(m):
        class_node = CLASS_START + j
        min_cap, max_cap = proposedClasses[j][1], proposedClasses[j][2]
        network.add_edge(class_node, SUPER_SINK, min_cap)
        network.add_edge(class_node, SINK, max_cap - min_cap)

    network.add_edge(SINK, SUPER_SINK, n - total_min)

    if network.ford_fulkerson() != n:
        return None

    allocation = [None] * n
    intermediate2_node = network.vertices[INTERMEDIATE2]

    for i in range(n):
        student_node = network.vertices[STUDENT_START + i]
        for edge in student_node.edges:
            if edge.flow > 0:
                if TIME_PREF_START <= edge.v < TIME_PREF_START + 20:
                    for edge2 in network.vertices[edge.v].edges:
                        if CLASS_START <= edge2.v < CLASS_START + m and edge2.flow > 0:
                            allocation[i] = edge2.v - CLASS_START
                            edge2.flow -= 1
                            break
                elif edge.v == INTERMEDIATE1:
                    for edge2 in intermediate2_node.edges:
                        if CLASS_START <= edge2.v < CLASS_START + m and edge2.flow > 0:
                            allocation[i] = edge2.v - CLASS_START
                            edge2.flow -= 1
                            break

    if None in allocation:
        return None

    return allocation
