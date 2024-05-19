"""GOOD CODE"""


class Kosaraju:
    def __init__(self, vertices):
        self.vertices = vertices
        self.adjacency_list = [[] for _ in range(vertices)]
        self.adjacency_list_transpose = [[] for _ in range(vertices)]

    def add_edge(self, src, dest):
        self.adjacency_list[src].append(dest)

    def dfs(self, vertex, visited, stack):
        visited[vertex] = True
        for neighbor in self.adjacency_list[vertex]:
            if not visited[neighbor]:
                self.dfs(neighbor, visited, stack)
        stack.append(vertex)

    def transpose_graph(self):
        for src in range(self.vertices):
            for dest in self.adjacency_list[src]:
                self.adjacency_list_transpose[dest].append(src)

    def dfs_scc(self, vertex, visited):
        visited[vertex] = True
        for neighbor in self.adjacency_list_transpose[vertex]:
            if not visited[neighbor]:
                self.dfs_scc(neighbor, visited)

    def kosaraju(self):
        stack = []
        visited = [False] * self.vertices

        for vertex in range(self.vertices):
            if not visited[vertex]:
                self.dfs(vertex, visited, stack)

        self.transpose_graph()

        visited = [False] * self.vertices
        num_scc = 0
        while stack:
            vertex = stack.pop()
            if not visited[vertex]:
                self.dfs_scc(vertex, visited)
                num_scc += 1
        print("Number of Strongly Connected Components:", num_scc)


def main():
    # Example graph represented as an adjacency list
    adj_list = {
        0: [1],
        1: [2],
        2: [0, 3],
        3: [4],
        4: [5, 6],
        5: [3],
        6: [7],
        7: [8],
        8: [6, 9],
        9: [10, 11],
        10: [12],
        11: [9],
        12: []
    }

    # Number of vertices
    V = len(adj_list)

    # Create an instance of Kosaraju's algorithm
    kosaraju = Kosaraju(V)

    # Add edges to the graph
    for src, destinations in adj_list.items():
        for dest in destinations:
            kosaraju.add_edge(src, dest)

    # Find the strongly connected components using Kosaraju's algorithm
    kosaraju.kosaraju()


if __name__ == "__main__":
    main()
