import math


class Graph:
    _vertices: int
    adj_list: dict
    weights: dict

    def __init__(self, filename: str):
        with open(filename, 'r') as file:

            self._vertices = int(file.readline())
            self.adj_list = dict()
            self.weights = dict()

            for x, line in zip(range(self._vertices), file):
                self.adj_list[x] = list()
                weights = map(int, line.split())

                for y, w in zip(range(self._vertices), weights):
                    if w > 0:
                        self.adj_list[x].append(y)
                        self.weights[(x, y)] = w

    def size(self):
        return self._vertices

    def is_connected(self):
        stack = {0}
        unconnected = set(range(1, self._vertices))

        while unconnected:
            if not stack:
                break
            v = stack.pop()
            for u in self.adj_list[v]:
                if u in unconnected:
                    stack.add(u)
                    unconnected.remove(u)
        else:
            return True
        return False

    # only for connected graph
    def kruskal(self):
        components = list(range(self._vertices))
        edges = dict(sorted(self.weights.items(), key=lambda item: item[1], reverse=True))
        tree_weight = 0
        tree = list()

        while len(tree) < self._vertices - 1:
            edge, weight = edges.popitem()
            edge_comps = (components[edge[0]], components[edge[1]])
            if edge_comps[0] != edge_comps[1]:
                tree_weight += weight
                tree.append(edge)
                for v, comp in enumerate(components):
                    if comp == edge_comps[1]:
                        components[v] = edge_comps[0]
        return tree_weight, tree

    # only for connected graph
    def prima(self):
        start_vert = 0
        tree = list()
        tree_weight = 0
        pretenders = {(start_vert, v) for v in self.adj_list[start_vert]}
        edge_from_tree = [((0, 0), math.inf)] * self._vertices
        for p in pretenders:
            edge_from_tree[p[1]] = (p, self.weights[p])

        edge_from_tree[0] = (edge_from_tree[0][0], -math.inf)

        while len(tree) < self._vertices - 1:
            edge = min(pretenders, key=lambda item: self.weights[item])
            new_vert = edge[1]

            pretenders.remove(edge)
            edge_from_tree[new_vert] = (edge, -math.inf)
            tree.append(edge)
            tree_weight += self.weights[edge]

            for v in self.adj_list[new_vert]:
                new_edge = (new_vert, v)
                if edge_from_tree[v][1] > self.weights[new_edge]:
                    pretenders.discard(edge_from_tree[v][0])
                    pretenders.add(new_edge)
                    edge_from_tree[v] = (new_edge, self.weights[new_edge])
        return tree_weight, tree
