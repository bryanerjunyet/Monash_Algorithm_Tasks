import heapq

class Edge:
    def __init__(self, u, v, cost, time):
        self.u = u
        self.v = v
        self.cost = cost
        self.time = time


class Vertex:
    def __init__(self, id):
        self.id = id
        self.edges = []
        self.distance = float('inf')
        self.time = float('inf')
        self.previous = None

    def add_edge(self, edge):
        self.edges.append(edge)


class MinHeap:
    def __init__(self, input_data):
        self.length = len(input_data)
        self.heap = [None] + input_data[:]
        self.pos = [i + 1 for i in range(len(input_data))]
        self._heapify()

    def _heapify(self):
        for i in range(self.length // 2, 0, -1):
            self._sink(i)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.pos[self.heap[i][1]] = i
        self.pos[self.heap[j][1]] = j

    def _rise(self, k):
        while k > 1 and self.heap[k][0] < self.heap[k // 2][0]:
            self._swap(k, k // 2)
            k //= 2

    def _smallest_child(self, k):
        if 2 * k == self.length or self.heap[2 * k][0] < self.heap[2 * k + 1][0]:
            return 2 * k
        return 2 * k + 1

    def _sink(self, k):
        while 2 * k <= self.length:
            child = self._smallest_child(k)
            if self.heap[k][0] <= self.heap[child][0]:
                break
            self._swap(k, child)
            k = child

    def extract_min(self):
        if self.length == 0:
            raise IndexError("Heap is empty")
        min_val = self.heap[1]
        self._swap(1, self.length)
        self.length -= 1
        self._sink(1)
        return min_val

    def update(self, vertex_id, new_cost):
        idx = self.pos[vertex_id]
        self.heap[idx] = (new_cost, vertex_id)
        self._rise(idx)

    def is_empty(self):
        return self.length == 0


def intercept(roads, stations, start, friendStart):
    num_locations = 0
    for road in roads:
        num_locations = max(num_locations, road[0]+1, road[1]+1)
    
    vertices = [Vertex(i) for i in range(num_locations)]

    for u, v, c, t in roads:
        edge = Edge(u, v, c, t)
        vertices[u].add_edge(edge)

    # Build station index and train loop timings
    station_indices = [s[0] for s in stations]
    station_times = [s[1] for s in stations]
    station_index_array = [-1] * num_locations
    for i in range(len(stations)):
        station_index_array[stations[i][0]] = i

    # Dijkstra’s using cost, with tie-breaker on time
    cost_array = [(float('inf'), i) for i in range(num_locations)]
    cost_array[start] = (0, start)

    position_array = [i + 1 for i in range(num_locations)]
    min_heap = MinHeap(cost_array)

    vertices[start].distance = 0
    vertices[start].time = 0

    best_result = None  # (cost, time, path)

    while not min_heap.is_empty():
        current_cost, u_id = min_heap.extract_min()
        u = vertices[u_id]

        for edge in u.edges:
            v = vertices[edge.v]
            new_cost = u.distance + edge.cost
            new_time = u.time + edge.time

            if new_cost < v.distance or (new_cost == v.distance and new_time < v.time):
                v.distance = new_cost
                v.time = new_time
                v.previous = u
                min_heap.update(v.id, new_cost)

                # Interception logic (only if v is a train station)
                v_station_idx = station_index_array[v.id]
                if v_station_idx != -1:
                    friend_idx = station_index_array[friendStart]
                    friend_time = 0
                    idx = friend_idx
                    while friend_time <= new_time:
                        if stations[idx][0] == v.id and friend_time == new_time:
                            # Build path
                            path = []
                            temp = v
                            while temp:
                                path.append(temp.id)
                                temp = temp.previous
                            path.reverse()
                            if (best_result is None or
                                new_cost < best_result[0] or
                                (new_cost == best_result[0] and new_time < best_result[1])):
                                best_result = (new_cost, new_time, path)
                            break
                        friend_time += station_times[idx]
                        idx = (idx + 1) % len(stations)

    return best_result


# Example test case from PDF
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

print(intercept(roads, stations, start, friendStart))

# Expected: (7, 9, [6, 7, 8, 3])

# python new requirement