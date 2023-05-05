import networkx as nx
from pygraphblas import Matrix
from project.task_9_draft import dijkstra
from project.sssp import bellman_ford


def test_dijkstra():
    DG = nx.DiGraph()
    DG.add_edge(0, 1)
    DG.add_edge(1, 3)
    DG.add_edge(3, 1)
    DG.add_edge(2, 0)
    actual = dijkstra(DG, 0)
    assert actual == [0, 1, float("inf"), 2]

    actual = dijkstra(DG, 1)
    assert actual == [float("inf"), 0, float("inf"), 1]

    actual = dijkstra(DG, 2)
    assert actual == [1, 2, 0, 3]

    actual = dijkstra(DG, 3)
    assert actual == [float("inf"), 1, float("inf"), 0]

    # тест с использованием ранее реализованного алгоритма bellman_ford
    for i in range(1, 150):
        g = nx.DiGraph(nx.generators.atlas.graph_atlas(i))
        adj_matrix = Matrix.from_scipy_sparse(nx.adjacency_matrix(g))
        for s in g.nodes:
            actual = dijkstra(g, s)
            expected = bellman_ford(adj_matrix, s)
            assert actual == expected
