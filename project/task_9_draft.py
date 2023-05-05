from typing import List
import networkx as nx


def dijkstra(graph: nx.DiGraph, start_vertex) -> List:
    if graph.number_of_nodes() == 0:
        raise Exception("Передан граф без вершин")
    if start_vertex >= graph.number_of_nodes():
        raise Exception("Неверно указан индекс стартовой вершины")

    d = [float("inf")] * graph.number_of_nodes()
    d[start_vertex] = 0
    visited = [False] * graph.number_of_nodes()

    while not all(visited):
        # из ещё не посещённых вершин выбирается вершина u, имеющая минимальную метку.
        not_visited = [i for i, is_visited in enumerate(visited) if not is_visited]
        u = min([(i, d[i]) for i in not_visited], key=lambda x: x[1])[0]
        # рассматриваем всевозможные маршруты, в которых u является предпоследним пунктом.
        for v in graph.successors(u):
            if not visited[v]:
                # +1 т.к. граф не взвешенный
                if d[u] + 1 < d[v]:
                    d[v] = d[u] + 1
        visited[u] = True
    return d
