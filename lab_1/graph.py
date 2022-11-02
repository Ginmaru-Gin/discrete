import itertools
import math
import numpy as np


class Graph:
    _vert_count: int
    _matrix: np.ndarray

    def __init__(self, filename: str):
        self._vert_count = int(np.genfromtxt(filename, max_rows=1))
        self._matrix = np.genfromtxt(filename, skip_header=1)
        self._matrix[self._matrix == 0] = math.inf
        np.fill_diagonal(self._matrix, 0)

    def size(self) -> int:
        return self._vert_count

    def get_matrix(self) -> np.ndarray:
        return self._matrix

    def edge(self, v_out: int, v_in: int) -> float:
        """returns weight of edge"""
        return self._matrix[v_out, v_in]

    def incidents(self, v) -> np.ndarray:
        """returns neighbours of vertex"""
        return np.array([u for u in range(self._vert_count) if self.edge(v, u) != math.inf])

    def dijkstra(self, v: int) -> np.ndarray:
        result = np.full(self._vert_count, math.inf)
        remaining = np.array(range(self._vert_count))

        result[v] = 0
        remaining = np.delete(remaining, np.where(remaining == v))

        for u in self.incidents(v):
            result[u] = self.edge(v, u)

        while remaining.size > 0:
            # TODO improve this search
            v = remaining[0]
            w = result[v]
            for i in remaining:
                if result[i] < w:
                    v = i
                    w = result[i]

            remaining = np.delete(remaining, np.where(remaining == v))
            for u in self.incidents(v):
                result[u] = min(result[u], result[v] + self.edge(v, u))

        return result

    def ford_bellman(self, v: int) -> np.array:
        result = np.full(self._vert_count, math.inf)
        result[v] = 0

        vertices = range(self._vert_count)
        for _ in range(self._vert_count):
            done = True
            for u, w in itertools.product(vertices, vertices):
                tmp = result[w]
                result[w] = min(result[w], result[u] + self.edge(u, w))
                if tmp != result[w]:
                    done = False
            if done:
                break
        else:
            print('[FORD-BELLMAN]: Graph has negative weights!')

        return result

    def floyd_warshall(self) -> np.ndarray:
        vertices = range(self._vert_count)
        result = np.full((self._vert_count, self._vert_count), math.inf)
        for i in vertices:
            for j in self.incidents(i):
                result[i, j] = self._matrix[i, j]

        tmp = result
        for k in vertices:
            result, tmp = tmp, result
            for i, j in itertools.product(vertices, vertices):
                result[i, j] = min(tmp[i, j], tmp[i, k] + tmp[k, j])

        return result
