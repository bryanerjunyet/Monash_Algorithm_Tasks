"""
:Module description:
This module is a program for driver to determine the best driving route to intercept your friend who 
is onboard a circle train line, where the interception happens at a train station at the same time
with the least cost and earliest time.

:Classes:
City    : A city graph with the concept of multiverse.
Location: A location in the city, which can be a regular location or a train station.
Road    : A road between two locations.
MinHeap : A MinHeap for efficient selection of the minimum cost location.

"""

__author__ = "Er Jun Yet"


class City:
    """
    This is the main class of the module that represents a city graph with multiple time states 
    or notably known as the multiverse, for each location in reality.
    :Class description:
        This is the main class of the module that represents a city graph, consisting of the 
        entire road network with train stations and incorperating the concept of multiverse,
        where each location in reality is constructed multiple times at multiple time layers
        in the multiverse, based on the maximum train loop duration, constructing a larger
        city graph with the consideration of different multiverse.  

    :Approach description:
        The purpose of such multi-city graph to be constructed allows repeated visits to the 
        same location at different multiverse of time, where each location in reality is cloned
        into multiple copies of the same location_no, utilising the modulo time concept, depending
        on the maximum train loop duration. These copies of the same location will all be interconnected
        using the same road information. Below is an example of how the multiverse is constructed:

              
                --> (A2) ---  [Multiverse A] = where the location 0 us at multiverse A
               /            \ 
         5,4  /              \    35,6  
             /                ----------> (B0)  [Multiverse B] = where the location 0 is not visited back, 
            (A1)<--------------(A0)        /                     but transitioning to new location 0's multiverse B
                      35,7                /     
           (B1)<-------------------------/
                      35,7

        With this modification of multi-city, dijkstra algorithm can be utilised easily to search for 
        all possible routes over time, allowing repeated routes that involves looping back.

    :Attributes:
        total_reality_location      (int)       : Total number of all locations in reality.
        total_multiverse            (int)       : Total number of all multiverse layers.
        total_multiverse_locations  (int)       : Total number of all locations in all multiverse.
        multiverse_locations   (List[Location]) : A list of all Location objects in multiverse.
        total_train_duration        (int)       : Total time for a train to loop through all stations.
        acum_train_duration       (List[int])   : Accumulated time for each station in the train loop.
        multiverse_count            (int)       : Equals total_train_duration. Represents total temporal layers.
        total_location              (int)       : Total number of nodes across all multiverse layers.
        locations           (List[Location])    : All Location nodes in the multiverse graph.
        station_position        (List[int])     : Maps each location number to its index in the station list.

    """
    def __init__(self, roads, stations, friend_start):
        """
        :Function description:
            A City constructor that constructs a city graph with the concept of multiverse.

        :Input:
            roads       (List[Tuple[int, int, int, int]]) : A list of roads in the city, where each road contains the start, end, cost, time of this road.
            stations    (List[Tuple[int, int]])           : A list of train stations in the city, where each station contains the station_no and time_travel of this station.
            friend_start (int)                            : Starting location number of the friend (on the train).

        :Time complexity:
            O(R + S + ML + MR) --> O(MR + ML) --> O(R + L)
            where R is the number of roads, L is the number of locations and M is number of multiverse layers.

        :Time complexity analysis:
            - O(R) to find the total number of locations in reality.
            - O(S) to process each train stations duration, and find the the total train loop duration, 
              accumulated train duration and track friend's position.
            - O(ML) to construct locations across multiverse.
            - O(MR) to construct roads across multiverse.
            Thus, the total time complexity is O(R + S + ML + MR). 
            However, as the total number of stations, S is a constant, with at most 20 stations in a city (according to specification)
            and M is a constant too, with at most 100 minutes of train loop duration, the overall time complexity can be simplified to O(R + L).

        :Space complexity:
            O(ML + MR) --> O(L + R) 
            where R is the number of roads, L is the number of locations and M is number of multiverse layers.

        :Space complexity analysis:
            Input space of O(L + R) for the input list of roads and locations/ stations to be constructed by City() constructor,
            and auxiliary space of O(ML + MR) for the storing of roads and locations in the city across all multiverse, which should be
            a constant, depending on the maximum duration of the entire train loop. Thus, the dominating space complexity is O(L + R).
            
        """
        # Total number of locations in reality
        total_reality_location = 0
        for start, end, cost, time in roads:
            total_reality_location = max(total_reality_location, start+1, end+1)
        self.total_reality_location = total_reality_location

        # Construction of train stations info
        station_duration = [0] * len(stations)
        for i in range(len(stations)):
            station_no, travel_time = stations[i]
            station_duration[i] = travel_time
        
        # Total duration of train loop
        self.total_train_duration = sum(station_duration)

        # Track friend's position
        friend_position = -1
        for i in range(len(stations)):
            station_no = stations[i][0]
            if station_no == friend_start:
                friend_position = i
                break

        # Track each accumulated train duration
        self.acum_train_duration = [0] * len(stations)
        duration = 0
        for i in range(len(stations)):
            self.acum_train_duration[friend_position] = duration
            duration += station_duration[friend_position]
            friend_position = (friend_position + 1) % len(stations)

        # Existence of multiverse
        self.total_multiverse = self.total_train_duration
        self.total_multiverse_location = self.total_reality_location * self.total_multiverse

        # Construction of locations across multiverse
        self.multiverse_locations = []
        for multiverse in range(self.total_multiverse):
            for location in range(self.total_reality_location):
                self.multiverse_locations.append(Location(location))

        # Construction of roads across multiverse
        for layer in range(self.total_multiverse):
            for start, end, cost, time in roads:
                starting = layer * self.total_reality_location + start
                multiverse = (layer + time) % self.total_multiverse
                ending = multiverse * self.total_reality_location + end
                self.multiverse_locations[starting].add_road(Road(starting, ending, cost, time))
    
    def dijkstra_search(self, start):
        """
        :Function description:
            Search for the least cost paths from start location across all multiverses.

        :Approach description:
            1. Constructs a MinHeap of locations with its costs
            2. Get the minimum cost location from the heap.
            3. Visit each outgoing roads from the current location.
            4. Select the value with the lowest cost and time.
            5. Update the heap with the new cost and time and continue comparing.

        :Input:
            start (int): Starting location number

        :Time complexity:
            O(R log L), where R is the number of roads and L is the number of locations.

        :Time complexity analysis:
            - O(L) to construct heap array for location costs
            - O(log L) to get the minimum cost location from heap
            - O(R) to explore each and every outgoing roads
            - O(log L) to update the heap for each road
            Thus, the overall time complexity is O(R log L).

        :Space complexity:
            O(R + L), where R is the number of roads and L is the number of locations.

        :Space complexity analysis:
            Input space of O(R) for the number of roads and auxiliary space of O(L) for location_cost. 

        """
        
        # Reset city cost for each location
        location_cost = self.reset_city(start)
        
        # Construction of MinHeap arranged by minimum cost
        location_heap = MinHeap(location_cost)
        
        while not location_heap.is_empty():
            # Choose location with lowest cost
            current_cost, location_no = location_heap.get_min()
            chosen_location = self.multiverse_locations[location_no]
            current_time = chosen_location.time
            
            if chosen_location.visited:
                continue
            chosen_location.visited = True
            
            # Visit each outgoing roads
            for road in chosen_location.outgoing_roads:     
                new_cost = current_cost + road.cost
                new_time = current_time + road.time
                next_location = self.multiverse_locations[road.end]
                another_cost = next_location.cost
                another_time = next_location.time

                # New cost or time lesser than current
                if (next_location.visited == False) and (new_cost < another_cost or (new_cost == another_cost and new_time < another_time)):
                    next_location.cost = new_cost
                    next_location.time = new_time
                    next_location.previous_location = chosen_location
                    location_heap.update(road.end, new_cost)
    
    def reset_city(self, start):
        """
        :Function description:
            Resets location heap of costs and times for all city locations for dijsktra algorithm.

        :Input:
            start (int): The starting location number

        :Output:
            list[tuple]: A list of tuples (cost, location_no) for initialising the MinHeap
        
        :Time complexity:
            O(L), where L is the number of locations.

        :Time complexity analysis:
            Linear time for reassigning each location's cost and time.
        
        :Space complexity:
            O(L), where L is the number of locations.

        :Space complexity analysis:
            Input space of O(L) for the number of locations and auxiliary space of O(L) for the location_cost list.

        """
        location_cost = []

        # Reset corresponding cost and time for each location
        for location_no in range(len(self.multiverse_locations)):
            if location_no != start:
                location_cost.append((float('inf'), location_no))
                self.multiverse_locations[location_no].cost = float('inf')
                self.multiverse_locations[location_no].time = float('inf')
            else: # start location cost and time only 0, the rest unsure
                location_cost.append((0, location_no))
                self.multiverse_locations[location_no].cost = 0
                self.multiverse_locations[location_no].time = 0

        return location_cost

class Road:
    """
    This class represents a road between two locations.
    """
    def __init__(self, start, end, cost, time):
        """
        :Function description:
            A Road constructor.

        :Input:
            start (int) : Start location no
            end (int)   : End location no
            cost (int)  : Travel cost of this road
            time (int)  : Travel time (mins) of this road

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
        :Function description:
            Returns a string representation of the Road object.

        :Output:
            str - A string representation descripting Road in the format "start --(cost, time)--> end"
        """
        return f"{self.start} --(cost: {self.cost}, time: {self.time})--> {self.end}"


class Location:
    """
    This class represents a regular location or a train station.
    """
    def __init__(self, location_no):
        """
        :Function description:
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
        :Function description:
            Returns a string representation of the Location object.

        :Output:
            str - A string descripting the location and its outgoing roads.

        """
        description = f"Location {self.location_no}"
        for road in self.outgoing_roads:
            description += f"\n• {str(road)}"
        return description

    def add_road(self, road):
        """
        :Function description:
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
            Input space of O(N) and auxiliary space of O(N).

        """
        self.outgoing_roads.append(road)


class MinHeap:
    """
    This class represents a MinHeap for efficient selection of the minimum cost vertex.
    """
    def __init__(self, locations) :
        """
        :Function description:
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
            Input space of O(N) and auxiliary space of O(N) for heap and position arrays.

        """
        self.length = len(locations)
        self.heap = [None] * (self.length + 1)
        self.position = list(range(1, self.length + 1)) # position map for updates
        self.heapify(locations)
    
    def __len__(self):
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
    
    def is_empty(self):
        """
        :Function description:
            Checks if heap is empty.

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
            Input space of O(N) and auxiliary space of O(1).

        """
        return len(self) == 0

    def heapify(self, locations):
        """
        :Function description:
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
            Input space of O(N) and auxiliary space of O(1).

        """
        # Add input data into the heap
        for i in range(self.length):
            self.heap[i + 1] = locations[i]  # heap starts from index 1
            self.position[locations[i][1]] = i + 1  # map location_no to its position in the heap
        # Perform bottom-up operation
        for i in range(self.length//2, 0, -1):
            self.sink(i)

    def get_min(self):
        """
        :Function description:
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
            O(1)
            
        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

        """
        if self.is_empty():
            raise IndexError("Heap is empty.")
        minimum = self.heap[1]

        # Swap the root with the last element
        self.heap[1], self.heap[self.length] = self.heap[self.length], self.heap[1]
        self.position[self.heap[1][1]], self.position[self.heap[self.length][1]] = 1, self.length

        self.length -= 1
        self.sink(1)
        return minimum
    
    def smallest_child(self, index):
        """
        :Function description:
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
            O(1)

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

        """
        left = 2 * index
        right = left + 1
        smallest = 0
        if left == self.length or self.heap[left][0] < self.heap[right][0]:
            smallest = left
        else:
            smallest = right
        return smallest

    def sink(self, index):
        """
        :Function description:
            Restores heap property by moving element down the heap.

        :Input:
            index (int): Index of the element to sink

        :Time complexity:
            O(log N), where N is the number of elements in MinHeap.

        :Time complexity analysis:
            Sinking an element involves traversing log N depth of the MinHeap.

        :Space complexity:
            O(1)

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

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

    def rise(self, index):
        """
        :Function description:
            Restores heap property by moving element up the heap.
            
        :Input:
            index (int): Rise element index in MinHeap

        :Time complexity:
            O(log N), where N is the number of elements in MinHeap.

        :Time complexity analysis:
            Rising an element involves traversing log N height of the MinHeap.

        :Space complexity:
            O(1)

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

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
        :Function description:
            Updates new cost for a location in MinHeap and restores heap property.

        :Input:
            location_no (int)   : Location to update
            new_cost (int)      : New cost to update to the location

        :Time complexity:
            O(log N)

        :Time complexity analysis:
            Logarithmic time for rise().

        :Space complexity:
            O(1)

        :Space complexity analysis:
            Input space of O(1) and auxiliary space of O(1).

        """
        position = self.position[location_no]
        self.heap[position] = (new_cost, location_no)
        self.rise(position)

def intercept(roads, stations, start, friend_start):
    """
    :Function description:
        Search for best intercept location to meet a friend on a train loop.

    :Approach description:
        1.  Construct a city of roads and stations of the entire multiverse, and 
            marking the friend start and train stations duration.
        2.  Run dijsktra algorithm to search for shortest path to each location 
            from driver's location.
        3.  Choose the correct intercept location, depending on the computation of 
            multiverse layer and location index.
        4.  Check each train station with the intercept location to be the same time.
        5.  Backtrack intercept route by checking the previous visited location and save it.
        6.  Check chosen intercept route is of lowest cost and earliest arrival time.

    :Input:
        roads       (List[Tuple[int, int, int, int]]) : A list of roads in the city, where each road contains the start, end, cost, time of this road.
        stations    (List[Tuple[int, int]])           : A list of train stations in the city, where each station contains the station_no and time_travel of this station.
        start       (int)                             : Starting location number of the driver.
        friend_start (int)                            : Starting location number of the friend (on the train).

    :Output:
        Tuple[int, int, List[int, int]] or None : The best interception route, containing the cost, time and the route.

    :Time complexity:
        O(R log L), where R is the number of roads and L is the number of locations.

    :Time complexity analysis:
        - O(R + L) for the construction of the city and the roads.
        - O(R log L) for the dijkstra search.
        - O(S) for the search of the best intercept route.
        - O(L) for the backtrack of the route.
        Thus, the overall time complexity is O(R log L).

    :Space complexity:
        O(R + L), where R is the number of roads and L is the number of locations.

    :Space complexity analysis:
        Input space of O(R) for the input list of roads to be constructed by City() constructor, 
        and auxiliary space of O(R + L) for the storing of roads and locations in the city.

    """
    intercept_route = None

    # Construction of city
    city = City(roads, stations, friend_start)
    # Shortest path for each location in city
    city.dijkstra_search(start)
    
    # Possible interceptions for each train station
    for station in range(len(stations)):
        # Accumulative time of this station
        arrival_time = city.acum_train_duration[station]

        # Best intercept location of which multiverse using modulus
        multiverse = arrival_time % city.total_multiverse

        # Best intercept location of which index 
        station_index = stations[station][0]
        location_index = station_index + (multiverse * city.total_reality_location)
        location = city.multiverse_locations[location_index]
        
        # Best intercept time using modulus
        intercept_time = location.time % city.total_train_duration
        
        # Intercept !!!! when same location, same time
        if arrival_time == intercept_time:
            route = []
            backtrack = location
            # Backtrack previous locations to build route
            while backtrack is not None:
                route.insert(0, backtrack.location_no)
                backtrack = backtrack.previous_location

            # Best result for least cost
            if (intercept_route is None) or (location.cost < intercept_route[0]):
                intercept_route = (location.cost, location.time, route)
            # Best result for least time when same cost
            elif location.cost == intercept_route[0]:
                if location.time < intercept_route[1]:
                    intercept_route = (location.cost, location.time, route)

    return intercept_route
