from graph import Graph
from time import time

if __name__ == '__main__':
    test_count: int = 6
    for i in range(1, test_count + 1):
        filename = 'test' + str(i) + '.txt'
        print(filename)
        g = Graph(filename)
        if not g.is_connected():
            print('graph is not connected')
            print('-' * 30)
            continue

        print('\nKRUSKAL')
        t = time()
        weight, tree = g.kruskal()
        print(time() - t)
        print(weight)

        print('\nPRIMA')
        t = time()
        weight, tree = g.prima()
        print(time() - t)
        print(weight)
        print('-' * 30)

    g = Graph('test1.txt')
