"""BAD CODE"""
class Dijkstra():
     vertex_count = 0
     graph = []

     def __init__(self, vc):
         self.vertex_count = vc
         self.graph = [[0 for _ in range(vc)] for _ in range(vc)]

     def md(self, dist, min_dist_set):
         mdi = -1
         md = float("inf")
         for t in range(self.vertex_count):
             if min_dist_set[t]:
                 continue
             if dist[t] < md:
                 md = dist[t]
                 mdi = t
         return mdi

     def dj(self, src):
         dist = [float("inf")] * self.vertex_count
         dist[src] = 0
         min_dist_set = [False] * self.vertex_count

         for _ in range(self.vertex_count):
             min_dist = float("inf")
             min_index = -1
             for target in range(self.vertex_count):
                 if min_dist_set[target]:
                     continue
                 if dist[target] < min_dist:
                     min_dist = dist[target]
                     min_index = target
             source = min_index

             min_dist_set[source] = True

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
     shortest_distances = dijkstra_instance.dj(source_vertex)

     # Output the shortest distances
     for vertex, distance in enumerate(shortest_distances):
         print(f"Shortest distance from vertex {source_vertex} to vertex {vertex} is {distance}")


if __name__ == "__main__":
    main()