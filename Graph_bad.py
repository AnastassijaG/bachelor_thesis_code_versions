# """
# In a directed graph, a strongly connected component is a set of vertices such
# that for any pairs of vertices u and v there exists a path (u-...-v) that
# connects them. A graph is strongly connected if it is a single strongly
# connected component.
# """
#
#
from collections import defaultdict

""" BAD CODE """
class Graph:
    def __init__(self, vertex_count):
     self.vertex_count = vertex_count
     self.graph = defaultdict(list)

    def add_edge(self, source, target):
     self.graph[source].append(target)

    def is_strongly_connected(self):
     visited = [False] * self.vertex_count
     self._dfs(0, visited)
     if visited == [True] * self.vertex_count:
         reversed_graph = Graph(self.vertex_count)
         for source, adjacent in self.graph.items():
             for target in adjacent:
                 reversed_graph.add_edge(target, source)
         visited = [False] * self.vertex_count
         self._dfs(0, visited)
         if visited == [True] * self.vertex_count:
             return True
     return False

    def _dfs(self, source, visited):
     visited[source] = True
     for adjacent in self.graph[source]:
         if not visited[adjacent]:
             self._dfs(adjacent, visited)


def main():
    # Test the Graph class
    graph = Graph(5)  # Create a graph with 5 vertices

    # Add some edges
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 0)

    # Check if the graph is strongly connected
    if graph.is_strongly_connected():
        print("The graph is strongly connected.")
    else:
        print("The graph is not strongly connected.")

    # Add another edge to make the graph strongly connected
    graph.add_edge(4, 1)

    # Check again if the graph is strongly connected
    if graph.is_strongly_connected():
        print("Now the graph is strongly connected.")
    else:
        print("The graph is still not strongly connected.")


if __name__ == '__main__':
    main()