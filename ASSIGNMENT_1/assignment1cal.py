import math

class Location:
    """
    This class represents a location in a city.
    """
    def __init__(self, id: int, train_position: int) -> None:
        """
        Function Description:
            This function is the constructor of the Location class.

        Input:
            id (int): The id of the location as integers (exp: 0, 1, 2, 3, ...).
            train_position (int): The current position of the train.

        Output:
            None

        Time Complexity:
            O(1)

        Time Complexity Analysis:
            Assigning values to field variables are constant time operations.

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Initialising field variables does not use additional space.
        """
        self.id = id
        self.friend_interceptable = False
        self.train_position = train_position
        self.cost = math.inf
        self.duration = math.inf
        self.travelled = False
        self.finalised = False
        self.previous_location = None
    
    def __gt__(self, other: 'Location') -> bool:
        """
        Function Description:
            This function performs a greater than comparison between two Locations. It compares the costs
            of the two locations. If it is the same, then it will compare the duration.

        Input:
            other (Location): The other Location object to compare with.

        Output:
            bool: Returns True if self is greater than other, otherwise returns False.

        Time Complexity:
            O(1)

        Time Complexity Analysis:
            Comparisons are constant time operations.

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Comparison operations does not use additional space.
        """
        return (self.cost, self.duration) > (other.cost, other.duration)
    
    def __lt__(self, other: 'Location') -> bool:
        """
        Function Description:
            This function performs a lesser than comparison between two Locations. It compares the costs
            of the two locations. If it is the same, then it will compare the duration.

        Input:
            other (Location): The other Location object to compare with.

        Output:
            bool: Returns True if self is lesser than other, otherwise returns False.

        Time Complexity:
            O(1)

        Time Complexity Analysis:
            Comparisons are constant time operations.

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Comparison operations does not use additional space.
        """
        return (self.cost, self.duration) < (other.cost, other.duration)
    
    def __ge__(self, other: 'Location') -> bool:
        """
        Function Description:
            This function performs a greater than or equals to comparison between two Locations. It compares 
            the costs of the two locations. If it is the same, then it will compare the duration.

        Input:
            other (Location): The other Location object to compare with.

        Output:
            bool: Returns True if self is greater than or equal to other, otherwise returns False.

        Time Complexity:
            O(1)

        Time Complexity Analysis:
            Comparisons are constant time operations.

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Comparison operations does not use additional space.
        """
        return (self.cost, self.duration) >= (other.cost, other.duration)

    def __le__(self, other: 'Location') -> bool:
        """
        Function Description:
            This function performs a lesser than or equal to comparison between two Locations. It compares 
            the costs of the two locations. If it is the same, then it will compare the duration.

        Input:
            other (Location): The other Location object to compare with.

        Output:
            bool: Returns True if self is lesser than or equal to other, otherwise returns False.

        Time Complexity:
            O(1)

        Time Complexity Analysis:
            Comparisons are constant time operations.

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Comparison operations does not use additional space.
        """
        return (self.cost, self.duration) <= (other.cost, other.duration)


class Road:
    """
    This class represents a road in a graph.
    """
    def __init__(self, source: Location, destination: Location, cost: int, duration: int) -> None:
        """
        Function Description:
            This function is the constructor of the Road class.

        Input:
            source (Location): The source Location of the road.
            destination (Location): The destination Location of the road.
            cost (int): The cost as integers to travel from source Location to destination Location.
            duration (int): The duration as integers to travel from source Location to destination Location.

        Output:
            None

        Time Complexity:
            O(1)

        Time Complexity Analysis:
            Assigning values to field variables are constant time operations.

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Initialising field variables does not use additional space.
        """
        self.source_location = source
        self.destination_location = destination
        self.cost = cost
        self.duration = duration


class MinHeap:
    """
    This class represents a custom MinHeap for Dijkstra's Algorithm. 
    
    The code of this MinHeap is taken from FIT 1088 and modified to suit Dijkstra's Algorithm. Modifications 
    include an index map array to keep track of indexes of all items in the heap for consant time access and 
    swapping of indexes of items when they are moved around in the MinHeap, such as during add, rise, sink and
    serve operations.
    """
    def __init__(self, size: int) -> None:
        """
        Function Description:
            This function is the constructor of the MinHeap class.

        Input:
            size (int): The size as integer for the MinHeap array.

        Output:
            None

        Time Complexity:
            O(N), where N is the size of self.array.

        Time Complexity Analysis:
            The time to initialise self.array depends on the its size.

        Space Complexity:
            O(N)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Additional memory used depends on the size of self.array.
        """
        self.index_map = [0] * (size)
        self.array = [None] * (size + 1)
        self.length = 0

    def rise(self, k: int) -> None:
        """
        Function Description:
            This function rises item at index k to the correct position in the MinHeap.

        Input:
            k (int): The position of the item to rise in MinHeap.

        Output:
            None

        Time Complexity:
            O(log N), where N is the number of items in the heap.

        Time Complexity Analysis:
            The worst case is when the item is at the bottom of the heap and it needs to rise to the root,
            moving through the depth of the heap, which is log N. 

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Swapping the items in the heap and updating the index map does not use additional space.
        """
        while k > 1 and self.array[k] < self.array[k // 2]:
            self.array[k], self.array[k // 2] = self.array[k // 2], self.array[k]

            # Update the index mapping aftr swapping
            parent_index = self.array[k].id
            current_index = self.array[k // 2].id
            self.index_map[parent_index] = k
            self.index_map[current_index] = k // 2

            k = k // 2

    def sink(self, k: int) -> None:
        """
        Function Description:
            This function sinks the item at index k to the correct position in the MinHeap.

        Input:
            k (int): The position of the item to sink in MinHeap.

        Output:
            None

        Time Complexity:
            O(log N), where N is the number of items in the heap.

        Time Complexity Analysis:
            The worst case is when the item is at the root and needs to sink to the bottom of the heap,
            moving through the depth of the heap, which is log N. 

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Swapping the items in the heap and updating the index map does not use additional space.
        """
        while 2 * k <= self.length:
            j = self.get_smallest_child_index(k)
            if self.array[k] <= self.array[j]:
                break

            self.array[k], self.array[j] = self.array[j], self.array[k]

            # Update the index mapping aftr swapping
            current_index = self.array[j].id
            child_index = self.array[k].id
            self.index_map[current_index] = j
            self.index_map[child_index] = k 

            k = j

    def get_smallest_child_index(self, k: int) -> int:
        """
        Function Description:
            This function returns the index of the smallest child of item at index k.

        Input:
            k (int): The position of the item (parent) to get the smallest child node index.

        Output:
            int: The index of the smallest child node of parent node at index k.

        Time Complexity:
            O(1)

        Time Complexity Analysis:
            Comparison of child nodes to find smallest child index take constant time.

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Comparison operations does not use additional space.
        """
        if 2 * k == self.length or self.array[k * 2] < self.array[k * 2 + 1]:
            return k * 2
        
        else:
            return k * 2 + 1
        
    def add(self, item: Location) -> None:
        """
        Function Description:
            This function adds the item to the MinHeap and rises it to the correct position

        Input:
            item (Location): The item to be added to the MinHeap.

        Output:
            None

        Time Complexity:
            O(log N), where N is the number of items in the heap.

        Time Complexity Analysis:
            Worst case is to rise the item from bottom of heap to the root, travelling the total
            depth of the heap, which is log N.

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Assignment of item at first empty position of self.array and rising it to correct position
            in heap does not use additional space.
        """
        self.length += 1
        self.array[self.length] = item
        self.index_map[item.id] = self.length
        self.rise(self.length)
        
    def serve(self) -> Location:
        """
        Function Description:
            This function removes the minimum element (root) form the MinHeap and returns it.

        Input:
            None

        Output:
            Location: The minimum Location (root) in the heap.

        Time Complexity:
            O(log N), where N is the number of items in the heap.

        Time Complexity Analysis:
            The worst case is when the new root (previous last item in the heap swapped with the 
            mminimum to remove it) needs to sink back to the bottom of the heap, travelling a total 
            depth of the heap, which is log N.

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            Swapping the root and last item in the heap and sinking the new root to the correct position
            does not use additional space.
        """
        removed_item: Location = self.array[1]
        self.array[1], self.array[self.length] = self.array[self.length], self.array[1]

        # Update the index mapping aftr swapping
        last_item = self.array[1].id
        first_item = self.array[self.length].id
        self.index_map[last_item] =  1
        self.index_map[first_item] = 0
        
        self.array[self.length] = None
        self.length -= 1
        self.sink(1)

        return removed_item

    def update(self, k: int, new_cost: int, new_duration: int, previous_location: Location) -> None:
        """
        Function Description:
            This function updates the item at index k with the minimum cost and duration, and to 
            the correct position.

        Input:
            k (int): the position of the item to update.
            new_cost (int): The current cost to reach the location.
            new_duration (int): The current duration to reach the location.
            previous_location (Location): The previous location of the current location.

        Output:
            None

        Time Complexity:
            O(log N), where N is the number of items in the heap.

        Time Complexity Analysis:
            The worst case is when the new cost is less than the current cost of the item at index k or
            the cost is the same but the new duration is less than the current duration. The item needs
            to be updated and rise to the correct positon. Worst case is when the item is at the bottom
            of the heap and needs to rise to the root, traveling a total depth of the heap, which is log N.

        Space Complexity:
            O(1)

        Space Complexity Analysis:
            All inputs of this function take constant space.
            Comparison, assignment and rise operations does not use additional space.
        """
        index = self.index_map[k]
        location: Location = self.array[index]

        # Update if the current cost or current duration is more than the new cost or new duration
        if (location.cost, location.duration) > (new_cost, new_duration):
            location.previous_location = previous_location
            location.cost = new_cost
            location.duration = new_duration
            self.rise(index)


class CityMap:
    """
    This class represents a city map, where the locations are vertices and the roads are edges.
    """
    def __init__(self, road_list: list[tuple[int, int, int, int]], 
                 station_list: list[tuple[int, int]], friend_start: int) -> None:
        """
        Function Description:
            This function is the constructor of the CityMap class.

        Approach Description:
            In my approach, I chose to model the city map as a graph, where the locations were represented by
            vertices and the roads were represented by edges. In addition, for each location, I also created 
            multiple copies of it, with each accounting for one unique position the train is in. The number of
            copies created for one single location depends on the total number of unique positions the train can 
            be in for any given time. This is done for all the other locations as well. Then, all locations are 
            joined by the roads to their respective destination locations. My approach to create the graph is as 
            below:

            1. Find the total number of unique positions the train can be in by calculating the total duration
               for the train to finish one loop, since the train moves to a new position after every minute of 
               travel. So, 5 minutes to reach the start would mean 5 unique positions.

            2. Loop through the road list and determine the last location id. For each road, we check if the 
               source location id is greater than the last location id, if it is, we update the value to the
               source location id. The same steps is done with the destination location id as well.

            3. Create the location_list with size equal to the total unique train positions. Each position of
               the array stores the list of locations that accounts for a particular train position. This is
               done so that the program have constant time access over all locations at any train positions
               to update the cost and duration when running Dijkstra's Algorithm to intercept the friend. 

            4. I repeatedly created the same list of locations, with each list accounting for one unique train
               position. Each list is stored in the location_list array at the index of the train position
               that they represent. 

            5. Then, I created a road_list with size equal to the total unique train positions. Each position
               of the array stores an adjacency list of roads, where each adjacency list stores outgoing roads
               of source locations that accounts for one particular train position.

            6. I then iterate through each unique position of the train and repeatedly create the roads and
               join the source location, where the train is at a specfic position to its respective destination
               location. The road is then stored in the adjacency lists. 

            7. Then, I loop through the station list to find the index of the station that the friend starts
               from. If the first station index is found early, we can terminate the loop.

            8. Lastly, I looped through each of the stations from the stations list, starting from the first
               station and access the location object by indexing the current train position followed by the 
               train station id. I then update the friend_interceptable attribute for that location object to 
               be True. After that, I will update the current train position by adding its current value with 
               the travel duration to reach the next station. This is done before every next iteration.
        
        Input:
            road_list (list[tuple[int, int, int, int]]): A list of roads represented by tuples. Each tuple
                stores the source location id, destination location id, cost and duration to travel the road.
            station_list (list[tuple[int, int]]): A list of train stattions represented by tuples. Each tuple
                stores the location id and the duration.
            friend_start (int): The location id where the friend starts from.

        Output:
            None

        Time Complexity:
            O(|R| + |L|), where |R| is the total number of roads in the city and |L| is the total number of 
            locations in the city.

        Time Complexity Analysis:
            The main complexity contribution is to initialise each adjacency list with the size equal to the 
            number of location, |L| and then storing all outgoing roads at the index of the source location
            id in that adjacency list. This process is repeated for all other adjacency lists. The number of 
            adjacency lists is the number of unique train position. Hence, the complexity for this would be 
            O(k(|R| + |L|)), where k is the number of unique train positions. 
            
            We know that the a train can travel at most 5 minutes to another train station and the upper bound 
            of the number of train stations is 20. So, there are at most 20 * 5 = 100 possible positions than 
            the train can be in at any given time. Therefore, we know that the upper bound of k would just be
            100. Since, k is now a constant value, the final complexity of this function remains at O(|R| + |L|).

        Space Complexity:
            O(|R| + |L|), where |R| is the total number of roads in the city and |L| is the total number of 
            locations in the city.

        Space Complexity Analysis:
            Input Space:
                road_list takes |R| input space.
                station_list takes |S| input space, where S represents the number of train stations.
                friend_start takes constant space.

            Auxiliary Space:
                The main contribution of auxiliary space is to store the road adjacency list for each train
                position. Each adjacency list takes up (|L| + |R|) space, where the list has length of |L|
                and stores |R| number of roads in total. Therefore, the space complexity is O(k(|L| + |R|)), 
                where k is the number of unique train positions. Since we know that k is a constant value, 
                the final complexity is just O(|R| + |L|).

            Space complexity would be O(|R| + |S| + |R| + |L|). We know that |S| <= |L|, because all train 
            stations are locations but not all locations are train stations. So overal space complexity would 
            be O(|R| + |L|).
        """
        # Find the total positions the train can be at in the city
        self.total_train_position = 0
        for _, duration in station_list:
            self.total_train_position += duration # Each duration is a position the train can be in

        # Find the last location id to create the location list
        last_location_id = 0
        for source_location_id, destination_location_id, *_ in road_list:
            if last_location_id < source_location_id:
                last_location_id = source_location_id

            if last_location_id < destination_location_id:
                last_location_id = destination_location_id

        # Create the location list with size (total train position * location count)
        self.location_count = last_location_id + 1
        self.location_list = [None] * self.total_train_position
        for i in range(len(self.location_list)):
            self.location_list[i] = [None] * self.location_count

        # Fill the location list with locations ranging from 0 to last location id for each train position
        for train_position in range(self.total_train_position):
            for id in range(self.location_count):
                self.location_list[train_position][id] = Location(id, train_position)

        # Stores the list of edges following an adjancency list implementation
        self.road_count = len(road_list)
        self.road_list = [None] * self.total_train_position
        for train_position in range(self.total_train_position):
            self.road_list[train_position] = [None] * self.location_count
            for road in road_list:
                source_location, destination_location, cost, duration = road
                if self.road_list[train_position][source_location] is None:
                    self.road_list[train_position][source_location] = []

                source: Location = self.location_list[train_position][source_location]
                destination_index = (train_position + duration) % self.total_train_position
                destination: Location = self.location_list[destination_index][destination_location]
                self.road_list[train_position][source_location].append(Road(source, destination, cost, duration))

        # Find the station where the friend starts from
        init_station_index = 0
        for i in range(len(station_list)):
            if station_list[i][0] == friend_start:
                init_station_index = i
                break

        # Update the train stations where we can intercept the friend, start from friend_start station
        index = init_station_index
        train_current_position = 0
        for _ in range(len(station_list)):
            train_station_id = station_list[index][0]
            train_station: Location = self.location_list[train_current_position][train_station_id] 
            train_station.friend_interceptable = True
               
            train_current_position += station_list[index][1]
            index = (index + 1) % len(station_list)


def intercept(road_list: list[tuple[int, int, int, int]], station_list: list[tuple[int, int]], 
              source: int, friend_start: int) -> tuple[int, int, list[Location]] | None:
        """
        Function Description:
            This method intercepts the friend through a least cost path using Dijkstra's Algorithm.

        Approach Description:
            In my approach, I chose to use Dijkstra's Algorithm to determine the least cost path to intercept
            my friend. This is because, Dijkstra allows to determine the shortest costs from a single source
            to all other locations, which suits the context of the problem we have here (intercepting the 
            friend from a starting location).

            1. I started by creating the city map graph by passing in the road_list, station_list and friend
               start as parameters. The created CityMap object is stored in the graph variable.

            2. I initialised a MinHeap of size total unique train positions * location count to store the 
               locations that the program has travelled but not yet finalised.

            3. Then, I reference the source location from the location_list and update the source location
               to have a cost and duration of 0, and self.travelled to be True as we have already travelled
               to it. Then, it wil be added to the MinHeap.

            4. We repeatedly serve the location with minimum costs from the MinHeap for each iteration until
               the MinHeap is empty. Each served minimum location will be finalised, meaning that the cost and
               duration to reach that location is the minimum and it will no longer be updated. This is done
               by updating the finalised attribute of that location to be True.

            5. Then, the program checks if the served minimum location's friend_interceptable attribute is True. 
               If it is, this means that we are at the same location as the friend, therefore the friend is 
               interceptable. Then, the program will perform backtracking and return a list of locations in order, 
               that we have been through to intercept the friend. Then, the program terminates and return the costs, 
               duration and the list of location to intercept the friend (starting from source).

            6. If we are not at the same location as the friend, we will continue by getting all the outgoing edges
               from the served minimum location. We iterate through each of the roads and check if the destination
               location has been finalised. If it is, them we continue with the next road. If it is not, we check
               if the destination location has been discovered (added to the heap). If it is not yet discovered, we
               update the cost and duration to reach that location and add it to the MinHeap. If is discovered, we
               check if the new cost to reach the destination location is smaller than the current. If it is, we
               update the cost and duration in the destination location to the new values and rise it to the correct 
               position.

            7. If the algorithm visited all the locations in the city map and it still can't find a location where 
               we are at the same location as the friend, it means that the friend is not interceptable, so we 
               return None and the program ends.

        Input:
            road_list (list[tuple[int, int, int, int]]): A list of roads represented by tuples. Each tuple
                stores the source location id, destination location id, cost and duration to travel the road.
            station_list (list[tuple[int, int]]): A list of train stattions represented by tuples. Each tuple
                stores the location id and the duration.
            source (int): The location id at which we start from.
            friend_start (int): The location id where the friend starts from.

        Output:
            tuple[int, int, list[Location]] | None: Returns a tuple where the first index is the cost, the 
            second index being the duration and the last index being a list of locations, that we travelled
            in order, to intercept the friend. Returns None if the friend is not interceptable.

        Time Complexity:
            O(|R| log |L|), where |R| is the total number of roads in the city and |L| is the total number of 
            locations in the city.

        Time Complexity Analysis:
            1. Creating the City Map takes O(|R| + |L|) time.

            2. Initialising the MinHeap tales O(k |L|), where k is the number of unique train positions. Since
               k is a constant (discussed previously), the complexity would just be O(|L|).

            3. Adding the source location to the MinHeap takes O(1) time as it is the first element added to
               MinHeap, no rise operation needed.

            4. Then, we will repeately serve the minimum location from the heap until it is empty. The worst
               case would be that we have to serve each location once. So, the complexity would be O(|L| log |L|).

            5. Then, we iterate through the roads from the served minimum location and add it to the heap if it
               has not been discovered or update the costs and duration if we find a new minimum and rises it to
               the correct position. The worst case would be that we have to go through each road once. For each
               road, we either add the destination location to the heap or update it with the new mnimum cost or
               duration. So, in total O(|R| log |L|) time cpmplexity.

            6. Lastly, backtracking to find the locations that we've been through takes O(|L|). Worst case would
               be that the least cost path to intercept the friend has to go through all locations. If the friend
               is not interceptable, this operation is not performed. 

            So the worst case complexity would be O(|R| + |L| + 1 + |L| log |L| + |R| log |L| + |L|). We simplify 
            the complexity to be O(|L| log |L| + |R| log |L|). We know that worst case would be that we have a dense
            graph, where |R| > |L|, so the complexity would just be O(|R| log |L|).

        Space Complexity:
            O(|R| + |L|), where |R| is the total number of roads in the city and |L| is the total number of 
            locations in the city.

        Space Complexity Analysis:
            Input Space:
                road_list takes |R| input space.
                station_list takes |S| input space, where S represents the number of train stations.
                friend_start takes constant space.

            Auxiliary Space:
                The main contribution of auxiliary space is when we create the CityMap graph. From the space
                complexity analysis above, we know that creating a CityMap takes O(|R| + |L|) space, so auxiliary
                space is O(|R| + |L|).

            Space complexity would be O(|R| + |S| + |R| + |L|). Since we already that |S| <= |L|, overall space 
            complexity would be O(|R| + |L|).
        """
        # Create the city map
        graph = CityMap(road_list, station_list, friend_start)

        travelled_heap = MinHeap(graph.location_count * graph.total_train_position)

        # We set the source to be travelled and have an initial cost and duration of 0
        source_location: Location = graph.location_list[0][source]
        source_location.travelled = True
        source_location.cost = 0
        source_location.duration = 0

        # Add the source location to the heap
        travelled_heap.add(source_location)

        # Run the algorithm until the heap does not have any locations left
        while travelled_heap.length != 0:

            # Serve the minimum location adn finalised it (no more update to cost and duration)
            min_location: Location = travelled_heap.serve()
            min_location.finalised = True

            # Check if we can intercept the friend at that location
            if min_location.friend_interceptable:
                total_duration = min_location.duration
                total_cost = min_location.cost

                # Backtrack the locations until we reach the initial locations
                backtrack_stack = []
                backtrack_stack.append(min_location.id)
                while min_location.previous_location is not None:
                    backtrack_stack.append(min_location.previous_location.id)
                    min_location = min_location.previous_location

                result = []
                while len(backtrack_stack) != 0:
                    result.append(backtrack_stack.pop())

                return total_cost, total_duration, result

            # Get the outgoing roads from location
            outgoing_roads: list[Road] = graph.road_list[min_location.train_position][min_location.id]
            
            # Check if minimum location have outgoing roads
            if outgoing_roads is not None:

                # Loop through each of the roads
                for road in outgoing_roads:

                    # We only want to update for non finalised locations
                    if road.destination_location.finalised == False:

                        # If the destination location not yet travelled, update the cost and duration 
                        # and add it to the heap
                        if road.destination_location.travelled == False:
                            road.destination_location.travelled = True
                            road.destination_location.cost = min_location.cost + road.cost
                            road.destination_location.duration = min_location.duration + road.duration
                            road.destination_location.previous_location = min_location
                            travelled_heap.add(road.destination_location)

                        # If it has been travelled, check if cost or duration is minimum
                        else:
                            new_cost = min_location.cost + road.cost
                            new_duration = min_location.duration + road.duration
                            travelled_heap.update(road.destination_location.id, new_cost, new_duration, min_location)

        return None
