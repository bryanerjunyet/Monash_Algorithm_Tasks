class MinHeap:
    """Min Heap implementation for Dijkstra's algorithm"""
    def __init__(self, max_size: int) -> None:
        self.length = 0
        self.the_array = [None] * (max_size + 1)
        self.position_map = [None] * max_size  # Maps vertex id to heap position

    def __len__(self) -> int:
        return self.length

    def is_empty(self) -> bool:
        return self.length == 0

    def rise(self, k: int) -> None:
        """Bubble up the element at index k to its correct position"""
        item = self.the_array[k]
        while k > 1 and item[0] < self.the_array[k // 2][0]:
            self.the_array[k] = self.the_array[k // 2]
            self.position_map[self.the_array[k][1]] = k
            k = k // 2
        self.the_array[k] = item
        self.position_map[item[1]] = k

    def smallest_child(self, k: int) -> int:
        """Returns the index of k's child with smallest value"""
        if 2 * k == self.length or self.the_array[2*k][0] < self.the_array[2*k+1][0]:
            return 2 * k
        else:
            return 2 * k + 1

    def sink(self, k: int) -> None:
        """Sink the element at index k to its correct position"""
        item = self.the_array[k]
        while 2 * k <= self.length:
            min_child = self.smallest_child(k)
            if self.the_array[min_child][0] >= item[0]:
                break
            self.the_array[k] = self.the_array[min_child]
            self.position_map[self.the_array[k][1]] = k
            k = min_child
        self.the_array[k] = item
        self.position_map[item[1]] = k

    def push(self, cost: int, vertex_id: int, time: int) -> None:
        """Add a new element to the heap"""
        if self.length >= len(self.the_array) - 1:
            raise IndexError("Heap is full")
        
        self.length += 1
        self.the_array[self.length] = (cost, vertex_id, time)
        self.position_map[vertex_id] = self.length
        self.rise(self.length)

    def pop(self) -> tuple:
        """Remove and return the minimum element"""
        if self.length == 0:
            raise IndexError("Heap is empty")
        
        min_elem = self.the_array[1]
        self.position_map[min_elem[1]] = None
        
        if self.length > 1:
            self.the_array[1] = self.the_array[self.length]
            self.position_map[self.the_array[1][1]] = 1
            self.sink(1)
        
        self.length -= 1
        return min_elem

    def update(self, vertex_id: int, new_cost: int, new_time: int) -> None:
        """Update the cost and time for a vertex"""
        pos = self.position_map[vertex_id]
        if pos is None:
            self.push(new_cost, vertex_id, new_time)
        else:
            old_cost, _, _ = self.the_array[pos]
            if new_cost < old_cost:
                self.the_array[pos] = (new_cost, vertex_id, new_time)
                self.rise(pos)

class Vertex:
    """Vertex class for graph representation"""
    def __init__(self, id: int):
        self.id = id
        self.edges = []  # List of (destination, cost, time) tuples
        self.visited = False
        self.cost = float('inf')
        self.time = float('inf')
        self.previous = None
        self.route = []

    def add_edge(self, v: int, cost: int, time: int):
        self.edges.append((v, cost, time))

def intercept(roads: list, stations: list, start: int, friendStart: int):
    """
    Finds the optimal path to intercept a friend on a train loop.
    
    Args:
        roads: List of (u, v, cost, time) tuples representing directed roads
        stations: List of (station_id, time_to_next) tuples in train loop order
        start: Starting location ID
        friendStart: Friend's starting station ID
    
    Returns:
        Tuple of (total_cost, total_time, route) or None if no solution
    """
    # Step 1: Build the graph and preprocess train stations
    num_locations = max(max(u for u, _, _, _ in roads), max(v for _, v, _, _ in roads)) + 1
    vertices = [Vertex(i) for i in range(num_locations)]
    
    for u, v, cost, time in roads:
        vertices[u].add_edge(v, cost, time)
    
    # Step 2: Precompute train station information
    station_ids = [s[0] for s in stations]
    station_times = [s[1] for s in stations]
    
    # Find friend's starting index in stations list
    try:
        friend_idx = station_ids.index(friendStart)
    except ValueError:
        return None  # Invalid friendStart
    
    # Precompute cumulative times from friend's starting position
    cumulative_times = [0] * len(stations)
    current_time = 0
    n = len(stations)
    for i in range(1, n):
        current_time += station_times[(friend_idx + i - 1) % n]
        cumulative_times[(friend_idx + i) % n] = current_time
    loop_time = cumulative_times[friend_idx] + station_times[(friend_idx + n - 1) % n]
    
    # Step 3: Modified Dijkstra's algorithm
    heap = MinHeap(num_locations)
    vertices[start].cost = 0
    vertices[start].time = 0
    vertices[start].route = [start]
    heap.push(0, start, 0)
    
    while not heap.is_empty():
        current_cost, u, current_time = heap.pop()
        u_vertex = vertices[u]
        
        if u_vertex.visited:
            continue
        u_vertex.visited = True
        
        # Check if we're at a station at same time as friend
        if u in station_ids:
            # Calculate friend's position at current_time
            mod_time = current_time % loop_time
            friend_pos_idx = None
            
            # Find which station friend is at or between
            for i in range(len(stations)):
                station_id = station_ids[(friend_idx + i) % n]
                arrival_time = cumulative_times[(friend_idx + i) % n]
                if mod_time == arrival_time and u == station_id:
                    # Interception successful
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

# Test cases from the assignment examples
def test_example1():
    roads = [(6,0,3,1), (6,7,4,3), (6,5,6,2), (5,7,10,5), (4,8,8,5), 
             (5,4,8,2), (8,9,1,2), (7,8,1,3), (8,3,2,3), (1,10,5,4), 
             (0,1,10,3), (10,2,7,2), (3,2,15,2), (9,3,2,2), (2,4,10,5)]
    stations = [(0,1), (5,1), (4,1), (3,1), (2,1), (1,1)]
    start = 6
    friendStart = 0
    result = intercept(roads, stations, start, friendStart)
    print(result)
    assert result == (7, 9, [6,7,8,3])
    print("Example 1 passed")

def test_example2():
    roads = [(0,1,35,3), (1,2,5,2), (2,0,35,4), (0,4,10,1), 
             (4,1,22,2), (1,5,65,1), (5,2,70,1), (2,3,10,1), (3,0,20,3)]
    stations = [(4,3), (5,2), (3,4)]
    start = 0
    friendStart = 4
    result = intercept(roads, stations, start, friendStart)
    assert result is None
    print("Example 2 passed")

def test_example3():
    roads = [(0,1,35,7), (1,2,5,4), (2,0,35,6), (0,4,10,5), 
             (4,1,22,3), (1,5,60,4), (5,3,70,2), (3,0,10,7)]
    stations = [(4,2), (5,1), (3,4)]
    start = 0
    friendStart = 3
    result = intercept(roads, stations, start, friendStart)
    assert result == (160, 39, [0,1,2,0,1,2,0,4])
    print("Example 3 passed")

def test_example4():
    roads = [(0,1,10,7), (0,2,10,3), (2,0,1,4), (1,0,1,7)]
    stations = [(2,4), (1,3)]
    start = 0
    friendStart = 1
    result = intercept(roads, stations, start, friendStart)
    assert result == (10, 3, [0,2])
    print("Example 4 passed")

if __name__ == "__main__":
    test_example1()
    test_example2()
    test_example3()
    test_example4()
    print("All tests passed")