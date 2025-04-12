class Edge:
    def __init__(self, u: int, v: int, cost: int, time: int):
        self.u = u
        self.v = v
        self.cost = cost
        self.time = time

class Vertex:
    def __init__(self, id: int):
        self.id = id
        self.edges = []
        self.is_station = False
        self.station_index = -1  # Only valid if is_station

class MinHeap:
    def __init__(self, max_size: int):
        self.length = 0
        self.the_array = [None] * (max_size + 1)
        self.position = [0] * max_size  # Tracks vertex positions in heap
    
    def __len__(self):
        return self.length
    
    def rise(self, k: int) -> None:
        item = self.the_array[k]
        while k > 1 and item[0] < self.the_array[k // 2][0]:
            self.the_array[k] = self.the_array[k // 2]
            self.position[self.the_array[k][1]] = k
            k = k // 2
        self.the_array[k] = item
        self.position[item[1]] = k
    
    def add(self, cost: int, vertex_id: int, time: int) -> None:
        self.length += 1
        self.the_array[self.length] = (cost, vertex_id, time)
        self.position[vertex_id] = self.length
        self.rise(self.length)
    
    def smallest_child(self, k: int) -> int:
        if 2 * k == self.length or self.the_array[2*k][0] < self.the_array[2*k+1][0]:
            return 2 * k
        else:
            return 2 * k + 1
    
    def sink(self, k: int) -> None:
        item = self.the_array[k]
        while 2 * k <= self.length:
            child = self.smallest_child(k)
            if self.the_array[child][0] >= item[0]:
                break
            self.the_array[k] = self.the_array[child]
            self.position[self.the_array[k][1]] = k
            k = child
        self.the_array[k] = item
        self.position[item[1]] = k
    
    def get_min(self):
        if self.length == 0:
            raise IndexError
        min_elem = self.the_array[1]
        self.position[min_elem[1]] = 0  # Mark as removed
        self.length -= 1
        if self.length > 0:
            self.the_array[1] = self.the_array[self.length + 1]
            self.position[self.the_array[1][1]] = 1
            self.sink(1)
        return min_elem
    
    def update(self, vertex_id: int, new_cost: int, new_time: int):
        pos = self.position[vertex_id]
        if pos == 0:  # Not in heap
            self.add(new_cost, vertex_id, new_time)
        else:
            old_cost = self.the_array[pos][0]
            if new_cost < old_cost:
                self.the_array[pos] = (new_cost, vertex_id, new_time)
                self.rise(pos)

class Graph:
    def __init__(self, num_vertices: int):
        self.vertices = [Vertex(i) for i in range(num_vertices)]
        self.stations = []
        self.train_loop_times = []
        self.total_train_loop_time = 0
    
    def add_edge(self, u: int, v: int, cost: int, time: int):
        self.vertices[u].edges.append(Edge(u, v, cost, time))
    
    def set_stations(self, stations: list):
        self.stations = stations
        # Precompute cumulative times for train loop
        self.train_loop_times = [0] * len(stations)
        for i in range(1, len(stations)):
            self.train_loop_times[i] = self.train_loop_times[i-1] + stations[i-1][1]
        self.total_train_loop_time = self.train_loop_times[-1] + stations[-1][1]
        
        # Mark stations in vertices
        for i, (station_id, _) in enumerate(stations):
            self.vertices[station_id].is_station = True
            self.vertices[station_id].station_index = i
    
    def get_friend_position(self, start_station_id: int, time: int) -> tuple:
        """Returns (station_id, remaining_time) where friend is at given time"""
        if not self.stations:
            return (None, 0)
        
        # Find which station index friend started at
        start_index = -1
        for i, (station_id, _) in enumerate(self.stations):
            if station_id == start_station_id:
                start_index = i
                break
        
        if start_index == -1:
            return (None, 0)
        
        # Calculate effective time in loop
        effective_time = time % self.total_train_loop_time
        current_time = 0
        current_index = start_index
        
        while True:
            next_index = (current_index + 1) % len(self.stations)
            segment_time = self.stations[current_index][1]
            
            if current_time + segment_time > effective_time:
                return (self.stations[current_index][0], effective_time - current_time)
            
            current_time += segment_time
            current_index = next_index
    
    def dijkstra_intercept(self, start: int, friend_start: int):
        # Initialize distances and previous nodes
        num_vertices = len(self.vertices)
        cost = [float('inf')] * num_vertices
        time = [float('inf')] * num_vertices
        previous = [-1] * num_vertices
        visited = [False] * num_vertices
        
        cost[start] = 0
        time[start] = 0
        heap = MinHeap(num_vertices)
        heap.add(0, start, 0)
        
        optimal_solution = None
        
        while len(heap) > 0:
            current_cost, u, current_time = heap.get_min()
            visited[u] = True
            
            # Check if current vertex is a station and if friend is here
            if self.vertices[u].is_station:
                friend_station, _ = self.get_friend_position(friend_start, current_time)
                if friend_station == u:
                    # Found a potential solution
                    if (optimal_solution is None or 
                        (current_cost < optimal_solution[0]) or 
                        (current_cost == optimal_solution[0] and current_time < optimal_solution[1])):
                        optimal_solution = (current_cost, current_time, u)
            
            # Early termination if we've found a solution and remaining paths are worse
            if optimal_solution and current_cost > optimal_solution[0]:
                continue
            
            for edge in self.vertices[u].edges:
                v = edge.v
                if visited[v]:
                    continue
                
                new_cost = cost[u] + edge.cost
                new_time = time[u] + edge.time
                
                if new_cost < cost[v] or (new_cost == cost[v] and new_time < time[v]):
                    cost[v] = new_cost
                    time[v] = new_time
                    previous[v] = u
                    heap.update(v, new_cost, new_time)
        
        if optimal_solution:
            # Reconstruct path
            path = []
            u = optimal_solution[2]
            while u != -1:
                path.append(u)
                u = previous[u]
            path.reverse()
            
            return (optimal_solution[0], optimal_solution[1], path)
        else:
            return None

def intercept(roads, stations, start, friend_start):
    # Find the maximum location ID to determine graph size
    max_loc = max(max(r[0], r[1]) for r in roads)
    for station in stations:
        if station[0] > max_loc:
            max_loc = station[0]
    if start > max_loc:
        max_loc = start
    if friend_start > max_loc:
        max_loc = friend_start
    
    num_vertices = max_loc + 1
    graph = Graph(num_vertices)
    
    # Add all roads
    for u, v, cost, time in roads:
        graph.add_edge(u, v, cost, time)
    
    # Set stations and train loop times
    graph.set_stations(stations)
    
    return graph.dijkstra_intercept(start, friend_start)

# Test cases from the assignment examples
if __name__ == "__main__":
    # Example 1
    roads1 = [(6,0,3,1), (6,7,4,3), (6,5,6,2), (5,7,10,5), (4,8,8,5), 
              (5,4,8,2), (8,9,1,2), (7,8,1,3), (8,3,2,3), (1,10,5,4), 
              (0,1,10,3), (10,2,7,2), (3,2,15,2), (9,3,2,2), (2,4,10,5)]
    stations1 = [(0,1), (5,1), (4,1), (3,1), (2,1), (1,1)]
    start1 = 6
    friend_start1 = 0
    print("Example 1:", intercept(roads1, stations1, start1, friend_start1))
    
    # Example 2 (unsolvable)
    roads2 = [(0,1,35,3), (1,2,5,2), (2,0,35,4), (0,4,10,1), 
              (4,1,22,2), (1,5,65,1), (5,2,70,1), (2,3,10,1), (3,0,20,3)]
    stations2 = [(4,3), (5,2), (3,4)]
    start2 = 0
    friend_start2 = 4
    print("Example 2:", intercept(roads2, stations2, start2, friend_start2))
    
    # Example 3
    roads3 = [(0,1,35,7), (1,2,5,4), (2,0,35,6), (0,4,10,5), 
              (4,1,22,3), (1,5,60,4), (5,3,70,2), (3,0,10,7)]
    stations3 = [(4,2), (5,1), (3,4)]
    start3 = 0
    friend_start3 = 3
    print("Example 3:", intercept(roads3, stations3, start3, friend_start3))
    
    # Example 4
    roads4 = [(0,1,10,7), (0,2,10,3), (2,0,1,4), (1,0,1,7)]
    stations4 = [(2,4), (1,3)]
    start4 = 0
    friend_start4 = 1
    print("Example 4:", intercept(roads4, stations4, start4, friend_start4))


# deep new requirement