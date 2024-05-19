# """
# In a directed graph, a strongly connected component is a set of vertices such
# that for any pairs of vertices u and v there exists a path (u-...-v) that
# connects them. A graph is strongly connected if it is a single strongly
# connected component.
# """
#
#
from collections import defaultdict


"""GOOD CODE"""

class Graph:
    def __init__(self, vertex_count):
        self.vertex_count = vertex_count
        self.adjacency_list = defaultdict(list)

    def add_edge(self, source, target):
        self.adjacency_list[source].append(target)

    def _dfs(self, source, visited):
        visited[source] = True
        for adjacent in self.adjacency_list[source]:
            if not visited[adjacent]:
                self._dfs(adjacent, visited)

    def _reverse_graph(self):
        reverse_adjacency_list = defaultdict(list)
        for source, adjacent in self.adjacency_list.items():
            for target in adjacent:
                reverse_adjacency_list[target].append(source)
        return reverse_adjacency_list

    def is_strongly_connected(self):
        def dfs_from(source):
            visited = [False] * self.vertex_count
            self._dfs(source, visited)
            return all(visited)

        if dfs_from(0):
            reversed_graph = Graph(self.vertex_count)
            reversed_graph.adjacency_list = self._reverse_graph()
            return dfs_from(0)
        return False

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