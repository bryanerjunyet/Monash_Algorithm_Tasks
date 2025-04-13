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



def dijkstra_search(locations, start, stations, station_position, station_duration, friend_start):
    """
    Function description:
        Runs Dijkstra's algorithm to determine the shortest cost path to intercept a friend on the train.
    :Input:
        locations: List of Location objects representing the city map
        start: int - The starting location no
        stations: List of tuples (station_no, time_to_next) representing train stations
        station_position: List[int] - Array mapping location nos to station indices
        station_duration: List[int] - List of travel times between consecutive stations
        friend_start: int - The train station where the friend starts
    :Output:
        Tuple[int, int, List[int]] or None - The best interception result (cost, time, route)
    :Time complexity:
        O(|R| log |L|)
    :Time complexity analysis:
        Where |R| is the number of roads and |L| is the number of locations. Each road is processed once, and heap operations are logarithmic in |L|.
    :Space complexity:
        O(|L| + |R|)
    :Space complexity analysis:
        Space is used for the locations, roads, and heap structures.
    """
    intercept_route = None 
    location_total = len(locations)
    location_cost = []

    # Initialise corresponding cost for each location
    for location_no in range(location_total):
        if location_no != start:
            location_cost.append((float('inf'), location_no))
        else: # start location cost and time only 0, the rest unsure
            location_cost.append((0, location_no))  
            locations[location_no].cost = 0
            locations[location_no].time = 0
    # Construction of MinHeap arranged by minimum cost
    location_heap = MinHeap(location_cost)

    while not location_heap.is_empty():
        # Choose location with lowest cost
        current_cost, location_no = location_heap.get_min()
        chosen_location = locations[location_no]
        current_time = chosen_location.time

        if chosen_location.visited:
            continue
        chosen_location.visited = True

        # Visit each outgoing roads
        for road in chosen_location.outgoing_roads:
            new_cost = current_cost + road.cost
            new_time = current_time + road.time
            next_location = locations[road.end]
            next_location_no = next_location.location_no
            another_cost = next_location.cost
            another_time = next_location.time

            # New cost or time lesser than current
            if (next_location.visited == False) and (new_cost <= another_cost) and (new_time < another_time):
                next_location.cost = new_cost
                next_location.time = new_time
                next_location.previous_location = chosen_location
                location_heap.update(next_location.location_no, new_cost)

                station_no = station_position[next_location_no]

                if station_no != -1: # Train station
                    start_no = station_position[friend_start]
                    friend_time = 0
                    friend_position = start_no

                    # Simulate friend's position from start to the location
                    while friend_time <= new_time:
                        # Intercept !!!! when same location, same time
                        if stations[friend_position][0] == next_location.location_no and friend_time == new_time:
                            location = next_location
                            route = []
                            # Backtrack previous locations to build route
                            while location is not None:
                                route.insert(0, location.location_no)
                                location = location.previous_location

                            # Best result for least cost
                            if (intercept_route is None) or (new_cost < intercept_route[0]):
                                intercept_route = (new_cost, new_time, route)
                            # Best result for least time when same cost
                            elif new_cost == intercept_route[0]:
                                if new_time < intercept_route[1]:
                                    intercept_route = (new_cost, new_time, route)
                            break  # Stop simulation

                        # Move friend to next station
                        friend_time += station_duration[friend_position]
                        friend_position = (friend_position + 1) % len(stations)

                else: # Not a station, continue next road
                    continue
        
        print(location_heap.heap)
        print(location_heap.position)

    return intercept_route


def intercept(roads, stations, start, friend_start):
    """
    Function description:
        Computes the optimal interception route to meet a friend on a train loop.
    :Input:
        roads: List of tuples (start, end, cost, time) representing the road network
        stations: List of tuples (station_no, time_to_next) representing train stations
        start: int - The starting location no
        friend_start: int - The train station where the friend starts
    :Output:
        Tuple[int, int, List[int]] or None - The best interception result (cost, time, route)
    :Time complexity:
        O(|R| log |L|)
    :Time complexity analysis:
        Where |R| is the number of roads and |L| is the number of locations. Dijkstra's algorithm dominates the complexity.
    :Space complexity:
        O(|L| + |R|)
    :Space complexity analysis:
        Space is used for the locations, roads, and heap structures.
    """
    locations = []
    total_location = 0

    print("Roads:", roads)
    # Total number of locations
    for road in roads:
        print(road)
        starting = road[0]
        ending = road[1]
        total_location = max(total_location, starting+1, ending+1)
    print("Total locations:", total_location)

    # Construction of all locations
    for i in range(total_location):
        new_location = Location(i)
        locations.append(new_location)

    # Construction of roads for each location
    for i in range(len(roads)):
        starting, ending, cost, time = roads[i]
        road = Road(starting, ending, cost, time)
        locations[starting].add_road(road)

    # Build station position and travel times arrays for freinds simulation
    station_position = [-1] * total_location
    station_duration = [0] * len(stations)

    for i in range(len(stations)):
        station_no, travel_time = stations[i]
        # just storing random numbers to indicate is a station
        station_position[station_no] = i 
        # store travel time between stations
        station_duration[i] = travel_time

    intercept_route = dijkstra_search(locations, start, stations, station_position, station_duration, friend_start)

    return intercept_route




# Example Test Case (from PDF)
roads = [(6,0,3,1), (6,7,4,3), (6,5,6,2), (5,7,10,5), (4,8,8,5), (5,4,8,2),
         (8,9,1,2), (7,8,1,3), (8,3,2,3), (1,10,5,4), (0,1,10,3), (10,2,7,2),
         (3,2,15,2), (9,3,2,2), (2,4,10,5)]
stations = [(0,1), (5,1), (4,1), (3,1), (2,1), (1,1)]
start = 6
friendStart = 0

# roads = [(0,1,35,7), (1,2,5,4), (2,0,35,6), (0,4,10,5), (4,1,22,3),
#             (1,5,60,4), (5,3,70,2), (3,0,10,7)]
# stations = [(4,2), (5,1), (3,4)]
# start = 0
# friendStart = 3

print(intercept(roads, stations, start, friendStart))
# Expected: (7, 9, [6, 7, 8, 3])
