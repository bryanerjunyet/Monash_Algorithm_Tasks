"""
Assignment 1 - Intercepting a Friend on a Train Loop
This program determines the least cost driving path to intercept a friend who is riding a circular train route.
The interception must occur at a train station at the exact same time, and you cannot wait at any location.

Approach:
- Use Dijkstra's algorithm to explore all possible driving paths.
- At each train station reached, calculate whether the friend arrives at the same time.
- Use a MinHeap to ensure efficient cost and time prioritization.

Time Complexity: O(|R| log |L|)
Space Complexity: O(|L| + |R|)
"""

class MultiGraph:
    def __init__(self, roads, stations, friend_start):
        # Initialize basic graph properties
        self.original_locations = max(max(r[0], r[1]) for r in roads) + 1
        self.stations = stations
        self.friend_start = friend_start
        
        # Calculate total train loop duration
        self.total_train_duration = sum(t for _, t in stations)
        
        # Initialize station position mapping
        self.station_position = [-1] * self.original_locations
        self.station_duration = [0] * len(stations)
        for i, (station_no, travel_time) in enumerate(stations):
            self.station_position[station_no] = i
            self.station_duration[i] = travel_time
        
        # Find friend's starting position index
        self.friend_start_index = -1
        for i, (station_no, _) in enumerate(stations):
            if station_no == friend_start:
                self.friend_start_index = i
                break
        
        # Precompute cumulative times from friend's starting position
        self.cumulative_times = [0] * len(stations)
        current_time = 0
        current_index = self.friend_start_index
        for i in range(len(stations)):
            self.cumulative_times[current_index] = current_time
            current_time += self.station_duration[current_index]
            current_index = (current_index + 1) % len(stations)
        
        # Initialize expanded graph (time-layered)
        self.max_time_layers = self.total_train_duration
        self.locations = []
        self._build_multi_graph(roads)
    
    def _build_multi_graph(self, roads):
        """Build the time-layered multi-graph"""
        # Each location is represented as (original_id * max_time_layers + time)
        total_expanded_locations = self.original_locations * (self.max_time_layers + 1)
        self.locations = [Location(i) for i in range(total_expanded_locations)]
        
        # Add roads considering time transitions
        for start, end, cost, time in roads:
            for t in range(self.max_time_layers + 1):
                remaining_time = t - time
                if remaining_time >= 0:
                    # Road can be taken within time limit
                    expanded_start = start * (self.max_time_layers + 1) + t
                    expanded_end = end * (self.max_time_layers + 1) + remaining_time
                    road = Road(expanded_start, expanded_end, cost, time)
                    self.locations[expanded_start].add_road(road)
    
    def get_original_location(self, expanded_id):
        """Convert expanded location ID back to original location ID"""
        return expanded_id // (self.max_time_layers + 1)
    
    def get_time_layer(self, expanded_id):
        """Get the time layer from expanded location ID"""
        return expanded_id % (self.max_time_layers + 1)
    
    def dijkstra_search(self, start):
        """Run Dijkstra's algorithm on the expanded graph"""
        expanded_start = start * (self.max_time_layers + 1) + 0  # Start at time layer 0
        
        location_cost = []
        for location_no in range(len(self.locations)):
            if location_no != expanded_start:
                location_cost.append((float('inf'), location_no))
            else:
                location_cost.append((0, location_no))
                self.locations[location_no].cost = 0
                self.locations[location_no].time = 0
        
        location_heap = MinHeap(location_cost)
        
        while not location_heap.is_empty():
            current_cost, location_no = location_heap.get_min()
            current_location = self.locations[location_no]
            
            if current_location.visited:
                continue
            current_location.visited = True
            
            for road in current_location.outgoing_roads:
                next_location = self.locations[road.end]
                
                if next_location.visited:
                    continue
                
                new_cost = current_cost + road.cost
                new_time = current_location.time + road.time
                
                if new_cost < next_location.cost or (new_cost == next_location.cost and new_time < next_location.time):
                    next_location.cost = new_cost
                    next_location.time = new_time
                    next_location.previous_location = current_location
                    location_heap.update(next_location.location_no, new_cost)

class Road:
    """
    This class represents a road between two locations.
    """
    def __init__(self, start, end, cost, time) -> None:
        """
        Function description:
            A Road constructor.
        :Input:
            start (int): Start location no
            end (int): End location no
            cost (int): Travel cost of this road
            time (int): Travel time (mins) of this road
        :Time complexity:
            O(1)
        :Time complexity analysis:
            Constant time for initialisation of Road attributes. 
        :Space complexity:
            O(1)
        :Space complexity analysis:
            Constant space for input and auxiliary.
        """
        self.start = start
        self.end = end
        self.cost = cost
        self.time = time
    
    def __str__(self):
        """
        Function description:
            Returns a string representation of the Road object.
        :Output:
            str - A string representation descripting Road in the format "start --(cost, time)--> end"
        """
        return f"{self.start} --(cost: {self.cost}, time: {self.time})--> {self.end}"


class Location:
    """
    This class represents a regular location or train station.
    """
    def __init__(self, location_no) -> None:
        """
        Function description:
            A Location constructor.
        :Input:
            location_no (int): Location number for tracking
        :Time complexity:
            O(1)
        :Time complexity analysis:
            Constant time for initialisation of Location attributes. 
        :Space complexity:
            O(1)
        :Space complexity analysis:
            Constant space for input and auxiliary.
        """
        self.location_no = location_no
        self.outgoing_roads = []
        self.cost = float('inf')  # minimum cost to reach this location
        self.time = float('inf')  # time taken to reach this location
        self.visited = False  # flag to check if location is visited
        self.previous_location = None  # pointer to reconstruct route
    
    def __str__(self):
        """
        Function description:
            Returns a string representation of the Location object.
        :Output:
            str - A string descripting the location and its outgoing roads.
        """
        description = f"Location {self.location_no}"
        for road in self.outgoing_roads:
            description += f"\n• {str(road)}"
        return description

    def add_road(self, road) -> None:
        """
        Function description:
            Add one outgoing road to a list of all for this location.
        :Input:
            road (Road): Road object to be added
        :Time complexity:
            O(1)
        :Time complexity analysis:
            Amortised complexity for append().
        :Space complexity:
            O(N), where N is the number of roads.
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1).
        """
        self.outgoing_roads.append(road)


class MinHeap:
    """
    This class represents a MinHeap for efficient selection of the minimum cost vertex.
    """
    def __init__(self, locations: list) -> None:
        """
        Function description:
            A MinHeap constructor to store an array of minimum cost to locations.
        :Input:
            locations (list[tuple]): List of tuples (cost, location_no)
        :Time complexity:
            O(N), where N is the number of locations.
        :Time complexity analysis:
            Linear time for heapify().
        :Space complexity:
            O(N), where N is the number of input locations.
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1) for heap and position arrays.
        """
        self.length = len(locations)
        self.heap = [None] * (self.length + 1)
        self.position = list(range(1, self.length + 1)) # position map for updates
        self.heapify(locations)
    
    def __len__(self) -> int:
        """
        Function description:
            Returns number of elements in heap array.
        :Input:
            None
        :Time complexity:
            O(1)
        :Time complexity analysis:
            Constant time for accessing the length attribute.
        :Space complexity:
            O(1)
        :Space complexity analysis:
            No additional space is used.
        """
        return self.length
    
    def is_empty(self) -> bool:
        """
        Function description:
            Checks if the heap is empty.
        :Input:
            None
        :Output:
            bool - True if heap array is empty, False otherwise
        :Time complexity:
            O(1)
        :Time complexity analysis:
            Constant time for checking the heap array empty or not.
        :Space complexity:
            O(N), where N is the number of input locations.
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1) for heap array.
        """
        return len(self) == 0

    def heapify(self, locations: list) -> None:
        """
        Function description:
            Bottom-up construction of MinHeap from an array of locations. 
        :Input:
            locations (list[tuple]): List of tuples (cost, location_no)
        :Time complexity:
            O(N), where N is the number of locations.
        :Time complexity analysis:
            Linear time for input locations and construction of MinHeap.
        :Space complexity:
            O(N), where N is the number of input locations.
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1) for heap and position arrays.
        """
        # Add input data into the heap
        for i in range(self.length):
            self.heap[i + 1] = locations[i]  # heap starts from index 1
            self.position[locations[i][1]] = i + 1  # map location_no to its position in the heap
        print(self.heap)
        print(self.position)
        # Perform bottom-up operation
        for i in range(self.length//2, 0, -1):
            self.sink(i)

    def get_min(self) -> tuple [int, int]:
        """
        Function description:
            Get minimum cost location from heap array.
        :Input:
            None
        :Output:
            Tuple[int, int] - Minimum cost and corresponding location
        :Time complexity:
            O(log N), where N is the number of elements in MinHeap.
        :Time complexity analysis:
            Logarithmic time for sink().
        :Space complexity:
            O(N), where N is the depth of the MinHeap.
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1) for heap array.
        """
        if self.is_empty():
            raise IndexError("Heap is empty.")
        print("----Heap----")
        print("MinHeap:", self.heap)
        minimum = self.heap[1]
        print("Minimum:", minimum)

        # Swap the root with the last element
        self.heap[1], self.heap[self.length] = self.heap[self.length], self.heap[1]
        self.position[self.heap[1][1]], self.position[self.heap[self.length][1]] = 1, self.length

        self.length -= 1
        print("After swap:", self.heap)
        self.sink(1)
        print("After sink:", self.heap)
        return minimum
    
    def smallest_child(self, index: int) -> int:
        """
        Function description:
            Find smallest child of a given parent node in MinHeap.
        :Input:
            index (int): Parent node index in MinHeap
        :Output:
            int - Smallest child node index
        :Time complexity:
            O(1)
        :Time complexity analysis:
            Constant time for comparisons to find smallest child.
        :Space complexity:
            O(N), where N is the depth of the MinHeap.
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1) for heap array.
        """
        left = 2 * index
        right = left + 1
        smallest = 0
        if left == self.length or self.heap[left][0] < self.heap[right][0]:
            smallest = left
        else:
            smallest = right
        return smallest

    def sink(self, index: int):
        """
        Function description:
            Restores heap property by moving element down the heap.
        :Input:
            index (int): Index of the element to sink
        :Time complexity:
            O(log N), where N is the number of elements in MinHeap.
        :Time complexity analysis:
            Sinking an element involves traversing log N depth of the MinHeap.
        :Space complexity:
            O(N)
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1) for heap array.
        """
        while 2 * index <= self.length:
            smallest = self.smallest_child(index)
            if self.heap[index][0] <= self.heap[smallest][0]:
                break
            else:
                # Swap the current element with its smallest child
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                self.position[self.heap[index][1]], self.position[self.heap[smallest][1]] = index, smallest

            index = smallest

    def rise(self, index: int):
        """
        Function description:
            Restores heap property by moving element up the heap.
        :Input:
            index (int): Rise element index in MinHeap
        :Time complexity:
            O(log N), where N is the number of elements in MinHeap.
        :Time complexity analysis:
            Rising an element involves traversing log N height of the MinHeap.
        :Space complexity:
            O(N)
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1) for heap array.
        """
        while index > 1:
            parent = index // 2
            if self.heap[index][0] < self.heap[parent][0]:
                # Swap the current element with its parent
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                self.position[self.heap[index][1]], self.position[self.heap[parent][1]] = index, parent
                index = parent
            else:
                break

    def update(self, location_no, new_cost):
        """
        Function description:
            Updates new cost for a location in MinHeap and restores heap property.
        :Input:
            location_no (int): Location to update
            new_cost (int): New cost to update to the location
        :Time complexity:
            O(log N)
        :Time complexity analysis:
            Logarithmic time for rise().
        :Space complexity:
            O(N), where N is the depth of the MinHeap.
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1) for heap array.
        """
        position = self.position[location_no]
        self.heap[position] = (new_cost, location_no)
        self.rise(position)

def intercept(roads, stations, start, friend_start):
    """
    Computes the optimal interception route to meet a friend on a train loop.
    :Input:
        roads: List of tuples (start, end, cost, time) representing the road network
        stations: List of tuples (station_no, time_to_next) representing train stations
        start: int - The starting location no
        friend_start: int - The train station where the friend starts
    :Output:
        Tuple[int, int, List[int]] or None - The best interception result (cost, time, route)
    """
    intercept_route = None

    # Construction of multi-graph
    city = MultiGraph(roads, stations, friend_start)
    city.dijkstra_search(start)
    
    print("Expanded:")
    for location in city.locations:
        print(f"Location No: {location.location_no}, Cost: {location.cost}, Time: {location.time}")

    # Check all possible stations for interception
    for station_no, _ in stations:
        station_index = city.station_position[station_no]
        if station_index == -1:
            continue
        
        # Check all time layers for this station
        for t in range(city.max_time_layers + 1):
            expanded_id = station_no * (city.max_time_layers + 1) + t
            location = city.locations[expanded_id]
            
            if location.cost == float('inf'):
                continue  # Skip unreachable states
            
            # Check if friend arrives at this station at this time
            if city.cumulative_times[station_index] == t:
                # Reconstruct the route
                route = []
                current_loc = location
                while current_loc is not None:
                    original_id = city.get_original_location(current_loc.location_no)
                    route.insert(0, original_id)
                    current_loc = current_loc.previous_location
                
                # Update best route if better
                if (intercept_route is None or 
                    (location.cost < intercept_route[0]) or 
                    (location.cost == intercept_route[0] and location.time < intercept_route[1])):
                    intercept_route = (location.cost, location.time, route)
    
    return intercept_route





# Example Test Case (from PDF)
roads = [(0,1,35,7), (1,2,5,4), (2,0,35,6), (0,4,10,5), (4,1,22,3),
            (1,5,60,4), (5,3,70,2), (3,0,10,7)]
stations = [(4,2), (5,1), (3,4)]
start = 0
friendStart = 3

print(intercept(roads, stations, start, friendStart))
# (160, 39, [0,1,2,0,1,2,0,4])
