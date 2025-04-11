class MinHeap:
    """
    Min Heap implementation for Dijkstra's algorithm
    """
    def __init__(self, input_data, max_vertex_id):
        """
        Initialize the min heap with input data
        :param input_data: List of tuples (cost, vertex_id, time)
        :param max_vertex_id: Maximum vertex ID to size position_map
        """
        self.length = len(input_data)
        self.array = [None] * (self.length + 1)  # 1-based indexing
        self.position_map = [None] * (max_vertex_id + 1)  # Maps vertex_id to heap position
        
        # Heapify the input data
        for i in range(self.length):
            self.array[i+1] = input_data[i]
            self.position_map[input_data[i][1]] = i+1
        
        # Bottom-up heap construction
        for i in range(self.length//2, 0, -1):
            self.sink(i)

    def __len__(self):
        return self.length

    def is_empty(self):
        return self.length == 0

    def rise(self, k):
        """Bubble up the element at index k"""
        item = self.array[k]
        while k > 1 and item[0] < self.array[k//2][0]:
            self.swap(k, k//2)
            k = k//2
        self.array[k] = item
        self.position_map[item[1]] = k

    def sink(self, k):
        """Sink the element at index k"""
        item = self.array[k]
        while 2*k <= self.length:
            child = self.smallest_child(k)
            if self.array[child][0] >= item[0]:
                break
            self.swap(child, k)
            k = child
        self.array[k] = item
        self.position_map[item[1]] = k

    def smallest_child(self, k):
        """Find the smallest child of node at index k"""
        if 2*k == self.length or self.array[2*k][0] < self.array[2*k+1][0]:
            return 2*k
        else:
            return 2*k+1

    def swap(self, i, j):
        """Swap elements at positions i and j"""
        self.array[i], self.array[j] = self.array[j], self.array[i]
        self.position_map[self.array[i][1]] = i
        self.position_map[self.array[j][1]] = j

    def extract_min(self):
        """Remove and return the minimum element"""
        if self.is_empty():
            raise IndexError("Heap is empty")
        
        min_elem = self.array[1]
        self.swap(1, self.length)
        self.length -= 1
        self.sink(1)
        return min_elem

    def update(self, vertex_id, new_cost, new_time):
        """Update the cost and time for a vertex"""
        pos = self.position_map[vertex_id]
        if pos is not None:
            self.array[pos] = (new_cost, vertex_id, new_time)
            self.rise(pos)

class Vertex:
    """
    Vertex class representing a location in the city
    """
    def __init__(self, id):
        self.id = id
        self.edges = []  # List of (destination, cost, time) tuples
        self.visited = False
        self.cost = float('inf')
        self.time = float('inf')
        self.previous = None
        self.route = []

    def add_edge(self, v, cost, time):
        self.edges.append((v, cost, time))

class TrainNetwork:
    """
    Class to manage the train loop information
    """
    def __init__(self, stations):
        self.station_ids = [s[0] for s in stations]
        self.station_times = [s[1] for s in stations]
        self.n = len(stations)
        
        # Precompute cumulative times
        self.cumulative_times = [0] * self.n
        for i in range(1, self.n):
            self.cumulative_times[i] = self.cumulative_times[i-1] + self.station_times[i-1]
        self.loop_time = self.cumulative_times[-1] + self.station_times[-1]
        
        # Create mapping from station id to its index
        self.station_index = {id: i for i, id in enumerate(self.station_ids)}

    def get_friend_position(self, start_station_id, current_time):
        """
        Calculate where the friend is at current_time
        Returns (station_id, arrival_time) if at a station, None otherwise
        """
        try:
            start_idx = self.station_index[start_station_id]
        except KeyError:
            return None
        
        mod_time = current_time % self.loop_time
        
        # Check if friend is exactly at a station at this time
        for i in range(self.n):
            station_id = self.station_ids[(start_idx + i) % self.n]
            arrival_time = self.cumulative_times[(start_idx + i) % self.n]
            if mod_time == arrival_time:
                return (station_id, arrival_time)
        
        return None

def intercept(roads, stations, start, friendStart):
    """
    Main function to find optimal interception path
    Returns: (total_cost, total_time, route) or None if no solution
    """
    # Step 1: Build the graph and find max vertex ID
    max_vertex_id = max(max(u for u, _, _, _ in roads), max(v for _, v, _, _ in roads))
    num_locations = max_vertex_id + 1
    vertices = [Vertex(i) for i in range(num_locations)]
    
    for u, v, cost, time in roads:
        vertices[u].add_edge(v, cost, time)
    
    # Step 2: Initialize train network
    train_net = TrainNetwork(stations)
    
    # Step 3: Modified Dijkstra's algorithm
    heap = MinHeap([(0, start, 0)], max_vertex_id)
    vertices[start].cost = 0
    vertices[start].time = 0
    vertices[start].route = [start]
    
    while not heap.is_empty():
        current_cost, u, current_time = heap.extract_min()
        u_vertex = vertices[u]
        
        if u_vertex.visited:
            continue
        u_vertex.visited = True
        
        # Check if we're at a station where friend arrives at same time
        if u in train_net.station_ids:
            friend_pos = train_net.get_friend_position(friendStart, current_time)
            if friend_pos is not None and friend_pos[0] == u:
                return (current_cost, current_time, u_vertex.route)
        
        # Explore all outgoing edges
        for v, cost, time in u_vertex.edges:
            v_vertex = vertices[v]
            new_cost = current_cost + cost
            new_time = current_time + time
            
            # Relaxation step
            if new_cost < v_vertex.cost or (new_cost == v_vertex.cost and new_time < v_vertex.time):
                v_vertex.cost = new_cost
                v_vertex.time = new_time
                v_vertex.previous = u
                v_vertex.route = u_vertex.route + [v]
                heap.update(v, new_cost, new_time)
    
    return None

# Test cases
def test_example1():
    roads = [(6,0,3,1), (6,7,4,3), (6,5,6,2), (5,7,10,5), (4,8,8,5), 
             (5,4,8,2), (8,9,1,2), (7,8,1,3), (8,3,2,3), (1,10,5,4), 
             (0,1,10,3), (10,2,7,2), (3,2,15,2), (9,3,2,2), (2,4,10,5)]
    stations = [(0,1), (5,1), (4,1), (3,1), (2,1), (1,1)]
    start = 6
    friendStart = 0
    result = intercept(roads, stations, start, friendStart)
    print("Example 1:", result)
    assert result == (7, 9, [6,7,8,3])

def test_example2():
    roads = [(0,1,35,3), (1,2,5,2), (2,0,35,4), (0,4,10,1), 
             (4,1,22,2), (1,5,65,1), (5,2,70,1), (2,3,10,1), (3,0,20,3)]
    stations = [(4,3), (5,2), (3,4)]
    start = 0
    friendStart = 4
    result = intercept(roads, stations, start, friendStart)
    print("Example 2:", result)
    assert result is None

def test_example3():
    roads = [(0,1,35,7), (1,2,5,4), (2,0,35,6), (0,4,10,5), 
             (4,1,22,3), (1,5,60,4), (5,3,70,2), (3,0,10,7)]
    stations = [(4,2), (5,1), (3,4)]
    start = 0
    friendStart = 3
    result = intercept(roads, stations, start, friendStart)
    print("Example 3:", result)
    assert result == (160, 39, [0,1,2,0,1,2,0,4])

def test_example4():
    roads = [(0,1,10,7), (0,2,10,3), (2,0,1,4), (1,0,1,7)]
    stations = [(2,4), (1,3)]
    start = 0
    friendStart = 1
    result = intercept(roads, stations, start, friendStart)
    print("Example 4:", result)
    assert result == (10, 3, [0,2])

if __name__ == "__main__":
    test_example1()
    test_example2()
    test_example3()
    test_example4()
    print("All tests passed")