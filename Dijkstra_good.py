"""GOOD CODE"""
class Graph:
    def __init__(self, vertex_count):
        self.vertex_count = vertex_count
        self.adjacency_matrix = [[0] * vertex_count for _ in range(vertex_count)]

    def find_min_distance_vertex(self, distances, visited):
        min_distance = float("inf")
        min_index = -1
        for vertex in range(self.vertex_count):
            if not visited[vertex] and distances[vertex] < min_distance:
                min_distance = distances[vertex]
                min_index = vertex
        return min_index

    def find_dijkstra_shortest_paths(self, source):
        distances = [float("inf")] * self.vertex_count
        distances[source] = 0
        visited = [False] * self.vertex_count

        for _ in range(self.vertex_count):
            source = self.find_min_distance_vertex(distances, visited)
            visited[source] = True

            for vertex in range(self.vertex_count):
                if not visited[vertex] and self.adjacency_matrix[source][vertex] != 0:
                    distances[vertex] = min(distances[vertex], distances[source] + self.adjacency_matrix[source][vertex])

        return distances

def main():
    # Create a graph with 5 vertices
    graph = Graph(5)

    # Define the adjacency matrix (example)
    adjacency_matrix = [
        [0, 10, 20, 0, 0],
        [10, 0, 5, 10, 0],
        [20, 5, 0, 0, 15],
        [0, 10, 0, 0, 20],
        [0, 0, 15, 20, 0]
    ]
    graph.adjacency_matrix = adjacency_matrix

    # Calculate shortest paths from vertex 0
    source_vertex = 0
    shortest_distances = graph.find_dijkstra_shortest_paths(source_vertex)

    # Output the shortest distances
    for vertex, distance in enumerate(shortest_distances):
        print(f"Shortest distance from vertex {source_vertex} to vertex {vertex} is {distance}")


if __name__ == "__main__":
    main()