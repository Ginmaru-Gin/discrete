import math
import numpy as np
from termcolor import colored


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
        result = self._matrix[v]
        remaining = np.array(range(self._vert_count))

        remaining = np.delete(remaining, np.where(remaining == v))

        while remaining.size > 0:
            v = remaining[result[remaining].argmin()]
            remaining = np.delete(remaining, np.where(remaining == v))
            tmp = self._matrix[v] + result[v]
            np.putmask(result, tmp < result, tmp)

        return result

    def ford_bellman(self, v: int) -> np.array:
        result = np.full(self._vert_count, math.inf)
        result[v] = 0

        for _ in range(self._vert_count):
            tmp = self._matrix + np.repeat(result, self._vert_count).reshape(self._vert_count, self._vert_count)
            old_result = result.copy()
            for u in range(self._vert_count):
                np.putmask(result, tmp[u] < result, tmp[u])
            if np.all(old_result == result):
                break
        else:
            print(colored('[FORD-BELLMAN]: Graph has negative weights!', 'red'))

        return result

    def floyd_warshall(self) -> np.ndarray:
        result = self._matrix.copy()

        for k in range(self._vert_count):
            tmp = np.tile(result[k], self._vert_count).reshape(self._vert_count, self._vert_count) + \
                    np.repeat(result[:, k], self._vert_count).reshape(self._vert_count, self._vert_count)
            np.putmask(result, tmp < result, tmp)

        return result
