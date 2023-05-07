import random

import networkx as nx
from pygraphblas import Matrix
from project.task_9_draft import dijkstra, DynamicSSSP
from project.sssp import bellman_ford


def test_dijkstra():
    # ручной тест
    g = nx.DiGraph()
    g.add_edge(0, 1)
    g.add_edge(1, 3)
    g.add_edge(3, 1)
    g.add_edge(2, 0)
    actual = dijkstra(g, 0)
    assert actual == [0, 1, float("inf"), 2]

    actual = dijkstra(g, 1)
    assert actual == [float("inf"), 0, float("inf"), 1]

    actual = dijkstra(g, 2)
    assert actual == [1, 2, 0, 3]

    actual = dijkstra(g, 3)
    assert actual == [float("inf"), 1, float("inf"), 0]

    # тест с использованием ранее реализованного алгоритма bellman_ford
    for i in range(1, 500):
        g = nx.to_directed(nx.generators.atlas.graph_atlas(i))
        adj_matrix = Matrix.from_scipy_sparse(nx.adjacency_matrix(g))
        for s in g.nodes:
            actual = dijkstra(g, s)
            expected = bellman_ford(adj_matrix, s)
            assert actual == expected


def test_dynamic():
    for i in range(1, 500):
        modifiable_graph: nx.DiGraph = nx.DiGraph(nx.generators.atlas.graph_atlas(i))

        edges = list(modifiable_graph.edges)
        del_edges_num = len(edges) // 2
        add_edges_num = len(edges) - del_edges_num

        # select edges that will be added to graph during test and fix their future insertion order
        add_edges = []
        for _ in range(add_edges_num):
            i = random.randint(0, len(edges) - 1)
            u, v = edges[i]
            add_edges.append(edges[i])
            modifiable_graph.remove_edge(u, v)
            del edges[i]

        # select edges that will be deleted from graph during test and fix their future deletion order
        del_edges = list(modifiable_graph.edges)
        # initialize distances for dynamic algorithm
        dynamic_sssp = DynamicSSSP(modifiable_graph, 0)

        while add_edges or del_edges:
            # add or delete edges in arbitrary order
            if add_edges and random.random() < 0.5:
                u, v = add_edges.pop()
                dynamic_sssp.add_edge(u, v)
            elif del_edges:
                u, v = del_edges.pop()
                dynamic_sssp.remove_edge(u, v)
            else:
                u, v = add_edges.pop()
                dynamic_sssp.add_edge(u, v)

            dynamic_sssp.update()
            expected = dijkstra(modifiable_graph, 0)

            assert dynamic_sssp.d == expected


def test_dynamic_decremental():
    for i in range(1, 500):
        modifiable_graph: nx.DiGraph = nx.DiGraph(nx.generators.atlas.graph_atlas(i))
        dynamic_sssp = DynamicSSSP(modifiable_graph, 0)
        edges = list(modifiable_graph.edges)
        while edges:
            i = random.randint(0, len(edges) - 1)
            u, v = edges[i]
            del edges[i]

            dynamic_sssp.add_edge(u, v)
            dynamic_sssp.update()
            expected = dijkstra(modifiable_graph, 0)

            assert dynamic_sssp.d == expected


def test_dynamic_incremental():
    for i in range(1, 500):
        g1: nx.DiGraph = nx.DiGraph(nx.generators.atlas.graph_atlas(i))

        modifiable_graph = nx.DiGraph()
        modifiable_graph.add_nodes_from(g1.nodes)

        dynamic_sssp = DynamicSSSP(modifiable_graph, 0)
        for u, v in g1.edges:
            dynamic_sssp.add_edge(u, v)

            dynamic_sssp.update()
            expected = dijkstra(modifiable_graph, 0)

            assert dynamic_sssp.d == expected
