"""BAD CODE"""
class Kosaraju:
    def __init__(self):
        self.vertices = 0
        self.adj = []

    def kosaraju(self, V, adj_list):
        stk, visited = [], [-1] * (V + 1)
        self.vertices = V
        self.adj = [[] for _ in range(V)]

        for src, dest_list in adj_list.items():
            for dest in dest_list:
                self.adj[src].append(dest)

        for i in range(V):
            if visited[i] == -1:
                visited[i] = 1
                stk.append(i)
                for x in self.adj[i]:
                    if visited[x] == -1:
                        stk.append(x)
                        visited[x] = 1
                        for y in self.adj[x]:
                            if visited[y] == -1:
                                stk.append(y)
                                visited[y] = 1
                                for z in self.adj[y]:
                                    if visited[z] == -1:
                                        stk.append(z)
                                        visited[z] = 1

        stk.reverse()
        res = stk.copy()

        ans, visited1 = 0, [-1] * (V + 1)

        adj1 = [[] for _ in range(V)]

        for i in range(len(self.adj)):
            for x in self.adj[i]:
                adj1[x].append(i)

        for i in range(len(res)):
            if visited1[res[i]] == -1:
                ans += 1
                for x in adj1[res[i]]:
                    visited1[x] = 1

        return ans

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
    kosaraju = Kosaraju()

    # Find the number of strongly connected components
    num_strongly_connected = kosaraju.kosaraju(V, adj_list)

    print(f"Number of strongly connected components: {num_strongly_connected}")

main()