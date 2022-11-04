from graph import Graph

import numpy as np
from scipy.sparse.csgraph import dijkstra, floyd_warshall
from termcolor import colored
from time import time


def test(filename: str, depth: int = 100):
    exec_time: float
    passed = lambda: print(colored('PASSED ' + str(exec_time), 'green'))
    not_passed = lambda: print(colored('NOT PASSED', 'red'))
    print('TEST: ', filename)

    g = Graph(filename)
    negative_weights = g.get_matrix().min() < 0
    vertices = range(0, g.size(), max(1, g.size() * depth // 100))

    if negative_weights:
        print(colored('NEGATIVE WEIGHTS', 'red'))
    else:
        check = dict()
        for v in vertices:
            check[v] = dijkstra(g.get_matrix(), indices=v)

        print('DIJKSTRA:')
        exec_time = time()
        for v in vertices:
            if np.array_equal(check[v], g.dijkstra(v)) is False:
                not_passed()
                break
        else:
            exec_time = time() - exec_time
            passed()

        print('FORD-BELLMAN:')
        exec_time = time()
        for v in vertices:
            if np.array_equal(check[v], g.ford_bellman(v)) is False:
                not_passed()
                break
        else:
            exec_time = time() - exec_time
            passed()

        check = floyd_warshall(g.get_matrix())
        print('FLOYD-WARSHALL:')
        exec_time = time()
        if np.array_equal(check, g.floyd_warshall()) is False:
            not_passed()
        else:
            exec_time = time() - exec_time
            passed()

    print()


if __name__ == '__main__':
    test_files = [
        'test.txt',
        'test1.txt',
        'test2.txt',
        'test3.txt',
        'test4.txt',
        'test5.txt'
    ]
    for file in test_files:
        test(file, 10)
        pass

    g = Graph('test3.txt')
    print('TEST FROD-BELLMAN FOR TEST_3 WITH NEGATIVE VALUES\n')
    for i in range(g.size()):
        t = time()
        g.ford_bellman(i)
        t = time() - t
        print('FORD-BELLMAN', t)
