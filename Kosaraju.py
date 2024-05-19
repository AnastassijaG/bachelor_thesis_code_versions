"""INITIAL CODE"""


class Kosaraju:

    def dfs(self, i, V, adj, visited, stk):
        visited[i] = 1

        for x in adj[i]:
            if visited[x] == -1:
                self.dfs(x, V, adj, visited, stk)

        stk.append(i)

    def kosaraju(self, V, adj):

        stk, visited = [], [-1]*(V+1)

        for i in range(V):
            if visited[i] == -1:
                self.dfs(i, V, adj, visited, stk)

        stk.reverse()
        res = stk.copy()

        ans, visited1 = 0, [-1]*(V+1)

        adj1 = [[] for x in range(V)]

        for i in range(len(adj)):
            for x in adj[i]:
                adj1[x].append(i)

        for i in range(len(res)):
            if visited1[res[i]] == -1:
                ans += 1
                self.dfs(res[i], V, adj1, visited1, stk)

        return ans


def main():
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




