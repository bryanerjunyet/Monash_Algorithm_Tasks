"""
FIT2004 Assignment 1 - Locomotion Commotion
Algorithm & Data Structure - Semester 1 2025
Author: <Your Name>
Student ID: <Your ID>

This solution follows the assignment constraints strictly:
- Time Complexity: O(|R| log |L|)
- Space Complexity: O(|L| + |R|)

Find the optimal (minimum cost, minimum driving time) driving path to intercept a friend on a moving train loop.
"""

# --------------------------- MinHeap Class ---------------------------
class MinHeap:
    """
    This is a class of MinHeap, a binary tree with the value of each node 
    less than or equal to the values of its children.
    The root node is the smallest element in the heap.
    """
    def __init__(self, max_size):
        # Initialize heap with fixed array size (1-indexed)
        self.length = 0  # Current number of elements
        self.the_array = [None] * (max_size + 1)  # Heap array (1-based indexing)

    def __len__(self):
        return self.length  # Return current heap size

    def is_empty(self):
        return self.length == 0  # Check if heap is empty

    def rise(self, k):
        # Bubble element up to maintain min-heap property
        item = self.the_array[k]
        while k > 1 and item < self.the_array[k // 2]:  # Compare with parent
            self.the_array[k] = self.the_array[k // 2]  # Move parent down
            k = k // 2  # Move up
        self.the_array[k] = item  # Insert at correct position

    def smallest_child(self, k):
        # Return index of smaller child
        if 2 * k == self.length or self.the_array[2 * k] < self.the_array[2 * k + 1]:
            return 2 * k
        else:
            return 2 * k + 1

    def sink(self, k):
        # Push element down to maintain min-heap
        item = self.the_array[k]
        while 2 * k <= self.length:
            min_child = self.smallest_child(k)
            if self.the_array[min_child] >= item:
                break  # Already in correct place
            self.the_array[k] = self.the_array[min_child]  # Move child up
            k = min_child
        self.the_array[k] = item  # Place item in correct position

    def add(self, element):
        # Add new element to heap
        self.length += 1
        self.the_array[self.length] = element
        self.rise(self.length)  # Restore heap

    def extract(self):
        # Remove and return smallest element
        if self.length == 0:
            raise IndexError("Heap is empty")
        min_elem = self.the_array[1]  # Smallest is at root
        self.the_array[1] = self.the_array[self.length]  # Replace root with last
        self.length -= 1
        if self.length > 0:
            self.sink(1)  # Restore heap
        return min_elem

# --------------------------- Edge Class ---------------------------
class Edge:
    def __init__(self, v, cost, time):
        self.v = v  # Destination vertex
        self.cost = cost  # Cost to traverse edge
        self.time = time  # Time to traverse edge

# --------------------------- Vertex Class ---------------------------
class Vertex:
    def __init__(self, id):
        self.id = id  # Unique identifier for the vertex
        self.edges = []  # List of outgoing edges

    def add_edge(self, v, cost, time):
        self.edges.append(Edge(v, cost, time))  # Add edge to vertex

# --------------------------- Graph Class ---------------------------
class Graph:
    def __init__(self, num_vertices):
        self.vertices = [Vertex(i) for i in range(num_vertices)]  # Initialize vertices

    def add_edge(self, u, v, cost, time):
        self.vertices[u].add_edge(v, cost, time)  # Add directed edge

# --------------------------- Train Class ---------------------------
class Train:
    def __init__(self, stations, friend_start, location_count):
        self.arrivals = [float('inf')] * location_count  # fixed-size array to simulate friend location over time
        idx = 0
        while stations[idx][0] != friend_start:
            idx += 1
        t = 0
        for i in range(len(stations)):
            station_id = stations[(idx + i) % len(stations)][0]
            self.arrivals[station_id] = t  # assigns exact time friend will arrive at this station
            t += stations[(idx + i) % len(stations)][1]

# class Train:
#     def __init__(self, stations, friend_start):
#         self.arrivals = self.compute_arrivals(stations, friend_start)  # Precompute train arrival times

#     def compute_arrivals(self, stations, friend_start):
#         arrival = {}  # Map from station to arrival time
#         time_elapsed = 0  # Time counter
#         idx = 0
#         while stations[idx][0] != friend_start:
#             idx += 1  # Locate friend's start station in list
#         n = len(stations)
#         for i in range(n):
#             station_id = stations[(idx + i) % n][0]  # Station ID in loop order
#             arrival[station_id] = time_elapsed  # Record arrival time
#             time_elapsed += stations[(idx + i) % n][1]  # Advance by time to next
#         return arrival  # Return map of station -> arrival time



# --------------------------- Pathfinder Class ---------------------------
class Pathfinder:
    def __init__(self, graph, start):
        self.graph = graph
        self.start = start
        self.dist = [float('inf')] * len(graph.vertices)  # Distance from start
        self.time = [float('inf')] * len(graph.vertices)  # Time from start
        self.prev = [None] * len(graph.vertices)  # Predecessor for path

    def dijkstra(self):
        self.dist[self.start] = 0  # Start has distance 0
        self.time[self.start] = 0  # Start has time 0
        heap = MinHeap(len(self.graph.vertices))  # Min heap for priority queue
        heap.add((0, 0, self.start))  # (cost, time, node)
        visited = [False] * len(self.graph.vertices)  # Track visited nodes

        while not heap.is_empty():
            cost_u, time_u, u = heap.extract()  # Extract min-cost node
            if visited[u]:
                continue  # Skip if already visited
            visited[u] = True
            for edge in self.graph.vertices[u].edges:
                v = edge.v  # Destination vertex
                new_cost = cost_u + edge.cost  # Cumulative cost
                new_time = time_u + edge.time  # Cumulative time
                if new_cost < self.dist[v] or (new_cost == self.dist[v] and new_time < self.time[v]):
                    self.dist[v] = new_cost  # Update best cost
                    self.time[v] = new_time  # Update best time
                    self.prev[v] = u  # Track path
                    heap.add((new_cost, new_time, v))  # Push to heap

    def recover_path(self, target):
        path = []
        while target is not None:
            path.append(target)  # Follow path backwards
            target = self.prev[target]  # Move to previous node
        return path[::-1]  # Reverse to get correct order

# --------------------------- Main Intercept Function ---------------------------
def intercept(roads, stations, start, friendStart):
    location_count = 0  # Track total number of locations
    for road in roads:
        location_count = max(location_count, road[0]+1, road[1]+1)  # Max vertex ID
    for station in stations:
        location_count = max(location_count, station[0]+1)

    graph = Graph(location_count)  # Initialize graph
    for u, v, cost, t in roads:
        graph.add_edge(u, v, cost, t)  # Add all roads

    train = Train(stations, friendStart, location_count)  # Create train simulation
    pathfinder = Pathfinder(graph, start)  # Path planner
    pathfinder.dijkstra()  # Run shortest path

    best_station = None
    best_cost = float('inf')
    best_time = float('inf')

    for station_id in range(location_count):
        if train.arrivals[station_id] != float('inf') and pathfinder.time[station_id] == train.arrivals[station_id]:
            if pathfinder.dist[station_id] < best_cost or (pathfinder.dist[station_id] == best_cost and pathfinder.time[station_id] < best_time):
                best_cost = pathfinder.dist[station_id]
                best_time = pathfinder.time[station_id]
                best_station = station_id

    if best_station is None:
        return None  # No valid interception

    route = pathfinder.recover_path(best_station)  # Recover path
    return (best_cost, best_time, route)  # Return result

# --------------------------- Test Case ---------------------------
if __name__ == "__main__":
    # Test example from assignment specification
    roads = [(6,0,3,1), (6,7,4,3), (6,5,6,2), (5,7,10,5), (4,8,8,5), (5,4,8,2),
             (8,9,1,2), (7,8,1,3), (8,3,2,3), (1,10,5,4), (0,1,10,3), (10,2,7,2),
             (3,2,15,2), (9,3,2,2), (2,4,10,5)]
    stations = [(0,1), (5,1), (4,1), (3,1), (2,1), (1,1)]
    start = 6
    friendStart = 0
    print(intercept(roads, stations, start, friendStart))  # Expected: (7, 9, [6, 7, 8, 3])
