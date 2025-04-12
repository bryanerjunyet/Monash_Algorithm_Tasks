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
        self.min_cost = float('inf')  # minimum cost to reach this location
        self.total_time = float('inf')  # time taken to reach this location
        self.previous_location = None  # pointer to reconstruct path

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
        for i in range(self.length // 2, 0, -1):
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
        if self.length == 0:
            raise IndexError("Heap is empty")
        minimum = self.heap[1]
        self.swap(1, self.length)
        self.length -= 1
        self.sink(1)
        return minimum
    
    def smallest_child(self, k: int) -> int:
        """
        Function description:
            Find smallest child of a given parent node in MinHeap.
        :Input:
            k (int): Parent node index in MinHeap
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
        if 2 * k == self.length or self.heap[2 * k][0] < self.heap[2 * k + 1][0]:
            return 2 * k
        else:
            return 2 * k + 1
    
    def swap(self, i: int, j: int) -> None:
        """
        Function description:
            Swaps two elements in heap array and updates positions in the position array.
        :Input:
            i (int): First element index to swap
            j (int): Second element index to swap
        :Time complexity:
            O(1)
        :Time complexity analysis:
            Constant time for reassigning of values in both heap and position arrays.
        :Space complexity:
            O(N), where N is the number of input locations.
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1) for heap and position arrays.
        """
        # Swap elements in heap array
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        # Update positions in position array
        self.position[self.heap[i][1]], self.position[self.heap[j][1]] = i, j

    def sink(self, k: int):
        """
        Function description:
            Restores heap property by moving element down the heap.
        :Input:
            k (int): Index of the element to sink
        :Time complexity:
            O(log N), where N is the number of elements in MinHeap.
        :Time complexity analysis:
            Sinking an element involves traversing log N depth of the MinHeap.
        :Space complexity:
            O(N)
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1) for heap array.
        """
        while 2 * k <= self.length:
            child = self.smallest_child(k)
            if self.heap[k][0] <= self.heap[child][0]:
                break
            self.swap(k, child)
            k = child

    def rise(self, k: int):
        """
        Function description:
            Restores heap property by moving element up the heap.
        :Input:
            k (int): Rise element index in MinHeap
        :Time complexity:
            O(log N), where N is the number of elements in MinHeap.
        :Time complexity analysis:
            Rising an element involves traversing log N height of the MinHeap.
        :Space complexity:
            O(N)
        :Space complexity analysis:
            Input space of O(N) and auxiliary space of O(1) for heap array.
        """
        while k > 1 and self.heap[k][0] < self.heap[k // 2][0]:
            self.swap(k, k // 2)
            k //= 2

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



def dijkstra_search(locations, start, stations, station_index_array, station_travel_times, friend_start_station):
    """
    Function description:
        Runs Dijkstra's algorithm to determine the shortest cost path to intercept a friend on the train.
    :Input:
        locations: List of Location objects representing the city map
        start: int - The starting location no
        stations: List of tuples (station_no, time_to_next) representing train stations
        station_index_array: List[int] - Array mapping location nos to station indices
        station_travel_times: List[int] - List of travel times between consecutive stations
        friend_start_station: int - The train station where the friend starts
    :Output:
        Tuple[int, int, List[int]] or None - The best interception result (cost, time, path)
    :Time complexity:
        O(|R| log |L|)
    :Time complexity analysis:
        Where |R| is the number of roads and |L| is the number of locations. Each road is processed once, and heap operations are logarithmic in |L|.
    :Space complexity:
        O(|L| + |R|)
    :Space complexity analysis:
        Space is used for the locations, roads, and heap structures.
    """
    num_locations = len(locations)
    cost_array = []

    # Initialize each location's cost as infinity except for the start
    for i in range(num_locations):
        if i == start:
            cost_array.append((0, i))  # cost to reach start is 0
            locations[i].min_cost = 0
            locations[i].total_time = 0
        else:
            cost_array.append((float('inf'), i))

    # Initialize the min heap with cost array
    min_heap = MinHeap(cost_array)
    best_result = None  # Store best result: (cost, time, path)

    # Start Dijkstra's loop
    while not min_heap.is_empty():
        # Get the location with the current lowest cost
        current_cost, current_location_no = min_heap.get_min()
        current_location = locations[current_location_no]

        # Traverse all outgoing roads from the current location
        for road in current_location.outgoing_roads:
            next_location = locations[road.end]
            new_cost = current_location.min_cost + road.cost
            new_time = current_location.total_time + road.time

            # Relax the edge if a cheaper path is found
            if new_cost < next_location.min_cost or (new_cost == next_location.min_cost and new_time < next_location.total_time):
                next_location.min_cost = new_cost
                next_location.total_time = new_time
                next_location.previous_location = current_location
                min_heap.update(next_location.location_no, new_cost)

                # Check if this next location is a train station
                station_no = station_index_array[next_location.location_no]
                if station_no != -1:
                    # Simulate the friend's position on the train loop
                    friend_no = station_index_array[friend_start_station]
                    friend_time = 0
                    friend_position = friend_no

                    while friend_time <= new_time:
                        # Interception condition: same location, same time
                        if stations[friend_position][0] == next_location.location_no and friend_time == new_time:
                            # Build the path to current location
                            path = []
                            current = next_location
                            while current is not None:
                                path.insert(0, current.location_no)
                                current = current.previous_location

                            # Update the best result based on cost and time
                            if best_result is None or new_cost < best_result[0] or (new_cost == best_result[0] and new_time < best_result[1]):
                                best_result = (new_cost, new_time, path)
                            break  # No need to simulate further

                        # Advance friend to next station
                        friend_time += station_travel_times[friend_position]
                        friend_position = (friend_position + 1) % len(stations)
        
        print(min_heap.heap)
        print(min_heap.position)

    return best_result


def intercept(roads, stations, start, friend_start_station):
    """
    Function description:
        Computes the optimal interception route to meet a friend on a train loop.
    :Input:
        roads: List of tuples (start, end, cost, time) representing the road network
        stations: List of tuples (station_no, time_to_next) representing train stations
        start: int - The starting location no
        friend_start_station: int - The train station where the friend starts
    :Output:
        Tuple[int, int, List[int]] or None - The best interception result (cost, time, path)
    :Time complexity:
        O(|R| log |L|)
    :Time complexity analysis:
        Where |R| is the number of roads and |L| is the number of locations. Dijkstra's algorithm dominates the complexity.
    :Space complexity:
        O(|L| + |R|)
    :Space complexity analysis:
        Space is used for the locations, roads, and heap structures.
    """
    num_locations = 0

    # Find total number of unique locations from road data
    for road in roads:
        from_location = road[0]
        to_location = road[1]
        if from_location + 1 > num_locations:
            num_locations = from_location + 1
        if to_location + 1 > num_locations:
            num_locations = to_location + 1

    # Create a list of location objects
    locations = []
    for i in range(num_locations):
        new_location = Location(i)
        locations.append(new_location)

    # Add road connections to each location
    for i in range(len(roads)):
        from_loc, to_loc, cost, time = roads[i]
        road = Road(from_loc, to_loc, cost, time)
        locations[from_loc].add_road(road)

    # Build station index array and travel times for simulation
    station_index_array = [-1] * num_locations
    station_travel_times = [0] * len(stations)

    for i in range(len(stations)):
        station_no, travel_time = stations[i]
        station_index_array[station_no] = i
        station_travel_times[i] = travel_time

    best_result = dijkstra_search(locations, start, stations, station_index_array, station_travel_times, friend_start_station)
    # Call the helper function to run Dijkstra and return best interception result

    return best_result




# Example Test Case (from PDF)
roads = [(6,0,3,1), (6,7,4,3), (6,5,6,2), (5,7,10,5), (4,8,8,5), (5,4,8,2),
         (8,9,1,2), (7,8,1,3), (8,3,2,3), (1,10,5,4), (0,1,10,3), (10,2,7,2),
         (3,2,15,2), (9,3,2,2), (2,4,10,5)]
stations = [(0,1), (5,1), (4,1), (3,1), (2,1), (1,1)]
start = 6
friendStart = 0
print(intercept(roads, stations, start, friendStart))
# Expected: (7, 9, [6, 7, 8, 3])
