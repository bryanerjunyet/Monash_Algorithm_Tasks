# Implementation for FIT2004 Assignment 1
# NOTE: No import, no dict/set used. Follows complexity and style rules strictly.

class Edge:
    def __init__(self, dest, cost, time):
        self.dest = dest
        self.cost = cost
        self.time = time

class Vertex:
    def __init__(self, idx):
        self.id = idx
        self.edges = []

class MinHeap:
    def __init__(self, input_data):
        self.length = len(input_data)
        self.the_array = [None] + input_data[:]
        self.build_heap()

    def __len__(self):
        return self.length

    def build_heap(self):
        for i in range(self.length // 2, 0, -1):
            self.sink(i)

    def rise(self, k):
        item = self.the_array[k]
        while k > 1 and item < self.the_array[k // 2]:
            self.the_array[k] = self.the_array[k // 2]
            k = k // 2
        self.the_array[k] = item

    def smallest_child(self, k):
        if 2 * k == self.length or self.the_array[2 * k] < self.the_array[2 * k + 1]:
            return 2 * k
        else:
            return 2 * k + 1

    def sink(self, k):
        item = self.the_array[k]
        while 2 * k <= self.length:
            child = self.smallest_child(k)
            if self.the_array[child] >= item:
                break
            self.the_array[k] = self.the_array[child]
            k = child
        self.the_array[k] = item

    def add(self, element):
        self.length += 1
        if self.length >= len(self.the_array):
            self.the_array.append(element)
        else:
            self.the_array[self.length] = element
        self.rise(self.length)

    def extract_min(self):
        if self.length == 0:
            raise IndexError("Heap is empty")
        min_elt = self.the_array[1]
        self.the_array[1] = self.the_array[self.length]
        self.length -= 1
        self.sink(1)
        return min_elt

    def is_empty(self):
        return self.length == 0

def intercept(roads, stations, start, friendStart):
    # Step 1: Build graph
    L = 0
    for u, v, _, _ in roads:
        L = max(L, u + 1, v + 1)

    graph = [Vertex(i) for i in range(L)]
    for u, v, cost, time in roads:
        graph[u].edges.append(Edge(v, cost, time))

    # Step 2: Simulate friend's train movement
    T = len(stations)
    station_to_index = [-1] * L
    loop_time = 0
    for i in range(T):
        station_to_index[stations[i][0]] = i
        loop_time += stations[i][1]

    friend_time_at_station = [[] for _ in range(L)]
    time = 0
    index = 0
    max_drive_time = 1000  # Upper bound simulation window
    while time <= max_drive_time:
        loc = stations[index][0]
        friend_time_at_station[loc].append(time)
        time += stations[index][1]
        index = (index + 1) % T

    # Step 3: Dijkstra to all reachable stations
    visited = [False] * L
    dist = [float('inf')] * L
    time_used = [float('inf')] * L
    prev = [-1] * L

    dist[start] = 0
    time_used[start] = 0
    heap_data = [(0, 0, start)]  # (total_cost, total_time, vertex_id)
    heap = MinHeap(heap_data)

    while not heap.is_empty():
        cost_u, time_u, u = heap.extract_min()
        if visited[u]:
            continue
        visited[u] = True

        for edge in graph[u].edges:
            v = edge.dest
            new_cost = cost_u + edge.cost
            new_time = time_u + edge.time

            if dist[v] > new_cost or (dist[v] == new_cost and time_used[v] > new_time):
                dist[v] = new_cost
                time_used[v] = new_time
                prev[v] = u
                heap.add((new_cost, new_time, v))

    # Step 4: Find best interception point
    best_cost = float('inf')
    best_time = float('inf')
    best_station = -1
    for s in range(L):
        if station_to_index[s] != -1:
            if dist[s] != float('inf'):
                for t in friend_time_at_station[s]:
                    if t == time_used[s]:
                        if dist[s] < best_cost or (dist[s] == best_cost and time_used[s] < best_time):
                            best_cost = dist[s]
                            best_time = time_used[s]
                            best_station = s

    if best_station == -1:
        return None

    # Step 5: Reconstruct path
    path = []
    current = best_station
    while current != -1:
        path.append(current)
        current = prev[current]
    path.reverse()

    return (best_cost, best_time, path)

# Example test case (from PDF Example 1)
roads = [(6,0,3,1), (6,7,4,3), (6,5,6,2), (5,7,10,5), (4,8,8,5), (5,4,8,2),
         (8,9,1,2), (7,8,1,3), (8,3,2,3), (1,10,5,4), (0,1,10,3), (10,2,7,2),
         (3,2,15,2), (9,3,2,2), (2,4,10,5)]
stations = [(0,1), (5,1), (4,1), (3,1), (2,1), (1,1)]
start = 6
friendStart = 0

# roads = [(0,1,35,3), (1,2,5,2), (2,0,35,4), (0,4,10,1), 
#             (4,1,22,2), (1,5,65,1), (5,2,70,1), (2,3,10,1), (3,0,20,3)]
# stations = [(4,3), (5,2), (3,4)]
# start = 0
# friendStart = 4

# roads = [(0,1,35,7), (1,2,5,4), (2,0,35,6), (0,4,10,5), 
#             (4,1,22,3), (1,5,60,4), (5,3,70,2), (3,0,10,7)]
# stations = [(4,2), (5,1), (3,4)]
# start = 0
# friendStart = 3

# roads = [(0,1,10,7), (0,2,10,3), (2,0,1,4), (1,0,1,7)]
# stations = [(2,4), (1,3)]
# start = 0
# friendStart = 1
print(intercept(roads, stations, start, friendStart))  # Expected: (7, 9, [6, 7, 8, 3])


# looks boleh