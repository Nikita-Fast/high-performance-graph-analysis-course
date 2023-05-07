import itertools
from typing import List
import networkx as nx
from boltons.queueutils import HeapPriorityQueue


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


class DynamicSSSP:
    # Алгоритм взят из статьи
    # An Incremental Algorithm for a Generalization of the Shortest-Path Problem
    # G. Ramalingam† and Thomas Reps‡

    def __init__(self, graph: nx.DiGraph, start_vertex: int):
        self._graph: nx.DiGraph = graph
        self._start_vertex = start_vertex
        self._modified_vertices = set()
        self._d = dijkstra(graph, start_vertex)

    def get_distances(self) -> List[int]:
        self._update()
        return self._d

    def _update(self):
        heap = HeapPriorityQueue(priority_key=lambda x: x)
        rhs = {}
        for u in self._modified_vertices:
            rhs[u] = self._compute_rhs(u)
            if rhs[u] != self._d[u]:
                key = min(rhs[u], self._d[u])
                heap.add(u, key)

        while heap:
            u = heap.pop()
            if rhs[u] < self._d[u]:
                self._d[u] = rhs[u]
                for v in self._graph.successors(u):
                    rhs[v] = self._compute_rhs(v)
                    if rhs[v] != self._d[v]:
                        key = min(rhs[v], self._d[v])
                        heap.add(v, key)
                    else:
                        if v in heap._entry_map:
                            heap.remove(v)
            else:
                self._d[u] = float("inf")
                for v in itertools.chain(self._graph.successors(u), [u]):
                    rhs[v] = self._compute_rhs(v)
                    if rhs[v] != self._d[v]:
                        key = min(rhs[v], self._d[v])
                        heap.add(v, key)
                    else:
                        if v in heap._entry_map:
                            heap.remove(v)

    def remove_edge(self, u, v):
        self._graph.remove_edge(u, v)
        self._modified_vertices.add(v)

    def add_edge(self, u, v):
        self._graph.add_edge(u, v)
        self._modified_vertices.add(v)

    def _compute_rhs(self, v):
        if v == self._start_vertex:
            return 0
        else:
            return (
                min(
                    (self._d[u] for u in self._graph.predecessors(v)),
                    default=float("inf"),
                )
                + 1
            )
