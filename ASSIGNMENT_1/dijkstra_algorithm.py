def dijkstra_2(self, source_id):
    class MinHeap(Generic[T]):

        def __init__(self, input_array, position_array) -> None:
            self.length = max_size = len(input_array) 
            self.array = [None] * (max_size+1)
            self.heapify(input_array)

            self.position_array = position_array
        
        def __len__(self) -> int:
            return self.length
        
        def rise(self, k: int) -> None:
            while k > 1 and self.array[k] < self.array[k//2]:
                self.swap(k, k//2)
                k = k // 2
        
        def swap(self, i, j):
            temp = self.array[i]
            self.array[i] = self.array[j]
            self.array[j] = temp

            vertex_id = self.array[i][1]
            self.position_array[vertex_id] = i
            vertex_id = self.array[j][1]
            self.position_array[vertex_id] = j

        def smallest_child(self, k: int) -> int:
            if 2*k == self.length or self.array[2*k] < self.array[2*k+1]:
                return 2*k
            else:
                return 2*k+1
            
        def is_empty(self) -> bool:
            return self.length == 0
            
        def sink(self, k: int) -> None:
            while 2*k <= self.length:
                child = self.smallest_child(k)
                if self.array[k] <= self.array[child]:
                    break
                self.swap(child, k)
                k = child
        
        def extract(self):
            if self.length == 0:
                raise IndexError

            min_elem = self.array[1]
            self.length -= 1
            if self.length > 0:
                self.swap(1, self.length+1)
                self.sink(1)
            return min_elem
        
        def heapify(self, input_array) -> None:
            for i in range(self.length):
                self.array[i + 1] = input_array[i]
            for i in range(self.length//2, 0, -1):
                self.sink(i)

        def update(self, vertex_id, new_distance):
            position = self.position_array[vertex_id]
            self.array[position] = (new_distance, vertex_id)
            self.rise(position)

    self.reset()

    position_array = [None] * len(self.vertices)
    input_array = [None] * len(self.vertices)
    for i in range(len(self.vertices)):
        vertex = self.vertices[i]
        if vertex.id == source_id:
            input_array[i] = (0, vertex.id)
            vertex.distance = 0
        else:
            input_array[i] = (float('inf'), vertex.id)
        position_array[i] = i+1
    min_heap = MinHeap(input_array, position_array)

    while not min_heap.is_empty():
        u_id = min_heap.extract()[1]
        u_vertex = self.vertices[u_id]

        for edge in u_vertex.edges:
            v_id = edge.v
            v_vertex = self.vertices[v_id]

            v_distance = v_vertex.distance
            new_distance = u_vertex.distance + edge.w
            if v_distance > new_distance:
                v_vertex.previous = u_vertex
                v_vertex.distance = new_distance
                min_heap.update(v_id, new_distance)

class Edge:
    def __init__(self, u: int, v: int, w: int=None):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        if self.w is None:
            resultStr = str(self.u) + " -----> " + str(self.v)
        else:
            resultStr = str(self.u) + " ---(" + str(self.w) + ")--> " + str(self.v)
        return resultStr

class Vertex:
    def __init__(self, id: int):
        self.id = id
        self.edges = LinkedList()    
        self.discovered = False
        self.visited = False
        self.distance = float('inf')
        self.previous = None
    
    def __str__(self):
        resultStr = "Vertex " + str(self.id)
        for edge in self.edges:
            resultStr = resultStr + "\n    " + str(edge)
        return resultStr
    
    def is_discovered(self):
        self.discovered = True
    
    def is_visited(self):
        self.visited = True
    
    def add_edge(self, edge: Edge):
        self.edges.append(edge)

if __name__ == "__main__":
    total_vertices = 5
    graph = Graph(total_vertices)
    
    edges = []
    edges.append((0, 1, 4))
    edges.append((0, 2, 2))
    edges.append((1, 2, 3))
    edges.append((1, 3, 2))
    edges.append((1, 4, 3))
    edges.append((2, 1, 1))
    edges.append((2, 3, 4))
    edges.append((2, 4, 5))
    edges.append((4, 3, 1))
    graph.add_edges(edges, True)

    graph.dijkstra_2(0)

    for vertex in graph.vertices:
        print(vertex.id, vertex.distance)