from graph import Graph
import numpy as np
from scipy.sparse.csgraph import dijkstra, floyd_warshall
from termcolor import colored


def test(filename: str, depth: int = 100):
    passed = lambda: print(colored('PASSED', 'green'))
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
        for v in vertices:
            if np.array_equal(check[v], g.dijkstra(v)) is False:
                not_passed()
                break
        else:
            passed()

        print('FORD-BELLMAN:')
        for v in vertices:
            if np.array_equal(check[v], g.ford_bellman(v)) is False:
                not_passed()
                break
        else:
            passed()

        check = floyd_warshall(g.get_matrix())
        print('FLOYD-WARSHALL:')
        if np.array_equal(check, g.floyd_warshall()) is False:
            not_passed()
        else:
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
