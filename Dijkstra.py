# INITIAL CODE #
class Dijkstra():
     """
     A fully connected directed graph with edge weights
     """

     def __init__(self, vertex_count):
         self.vertex_count = vertex_count
         self.graph = [[0 for _ in range(vertex_count)] for _ in range(vertex_count)]

     def min_distance(self, dist, min_dist_set):
         """
         Find the vertex that is closest to the visited set
         """
         min_dist = float("inf")
         for target in range(self.vertex_count):
             if min_dist_set[target]:
                 continue
             if dist[target] < min_dist:
                 min_dist = dist[target]
                 min_index = target
         return min_index

     def dijkstra(self, src):
         """
         Given a node, returns the shortest distance to every other node
         """
         dist = [float("inf")] * self.vertex_count
         dist[src] = 0
         min_dist_set = [False] * self.vertex_count

         for _ in range(self.vertex_count):
             #minimum distance vertex that is not processed
             source = self.min_distance(dist, min_dist_set)

             #put minimum distance vertex in shortest tree
             min_dist_set[source] = True

             #Update dist value of the adjacent vertices
             for target in range(self.vertex_count):
                 if self.graph[source][target] <= 0 or min_dist_set[target]:
                     continue
                 if dist[target] > dist[source] + self.graph[source][target]:
                     dist[target] = dist[source] + self.graph[source][target]

         return dist

def main():
     # Create an instance of Dijkstra class
     dijkstra_instance = Dijkstra(5)

     # Define the adjacency matrix (example)
     dijkstra_instance.graph = [
         [0, 10, 20, 0, 0],
         [10, 0, 5, 10, 0],
         [20, 5, 0, 0, 15],
         [0, 10, 0, 0, 20],
         [0, 0, 15, 20, 0]
     ]

     # Calculate shortest paths from vertex 0
     source_vertex = 0
     shortest_distances = dijkstra_instance.dijkstra(source_vertex)

     # Output the shortest distances
     for vertex, distance in enumerate(shortest_distances):
         print(f"Shortest distance from vertex {source_vertex} to vertex {vertex} is {distance}")


if __name__ == "__main__":
    main()

