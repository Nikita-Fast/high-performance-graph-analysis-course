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
    def __init__(self, graph: nx.DiGraph, start_vertex: int):
        self.graph: nx.DiGraph = graph
        self.start_vertex = start_vertex
        self.modified_vertices = set()
        self.d = dijkstra(graph, start_vertex)

    def update(self):
        heap = HeapPriorityQueue(priority_key=lambda x: x)
        rhs = {}
        for u in self.modified_vertices:
            rhs[u] = self.compute_rhs(u)
            if rhs[u] != self.d[u]:
                key = min(rhs[u], self.d[u])
                heap.add(u, key)

        while heap:
            u = heap.pop()
            if rhs[u] < self.d[u]:
                self.d[u] = rhs[u]
                for v in self.graph.successors(u):
                    rhs[v] = self.compute_rhs(v)
                    if rhs[v] != self.d[v]:
                        key = min(rhs[v], self.d[v])
                        heap.add(v, key)
                    else:
                        if v in heap._entry_map:
                            heap.remove(v)
            else:
                self.d[u] = float("inf")
                for v in itertools.chain(self.graph.successors(u), [u]):
                    rhs[v] = self.compute_rhs(v)
                    if rhs[v] != self.d[v]:
                        key = min(rhs[v], self.d[v])
                        heap.add(v, key)
                    else:
                        if v in heap._entry_map:
                            heap.remove(v)

    def remove_edge(self, u, v):
        self.graph.remove_edge(u, v)
        self.modified_vertices.add(v)

    def add_edge(self, u, v):
        self.graph.add_edge(u, v)
        self.modified_vertices.add(v)

    def compute_rhs(self, v):
        if v == self.start_vertex:
            return 0
        else:
            return (
                min(
                    (self.d[u] for u in self.graph.predecessors(v)),
                    default=float("inf"),
                )
                + 1
            )


# def rhs(graph: nx.DiGraph, vertex, d: List):
#     # todo добавить параметр start_vertex в метод update
#     if vertex == 0:
#         return 0
#     dists = [d[v] for v in graph.predecessors(vertex)]
#     if not dists:
#         return float('inf')
#     else:
#         return min(dists) + 1
#
#
# def dynamic_dijkstra(graph: nx.DiGraph, q: List, d: List):
#     while q:
#         _, u = heapq.heappop(q)
#         if rhs(graph, u, d) < d[u]:
#             d[u] = rhs(graph, u, d)
#         elif d[u] < rhs(graph, u, d):
#             d[u] = float('inf')
#
#
# def process_subtree(graph: nx.DiGraph, root, d: List, spt: nx.DiGraph):
#     s = set()
#     cur = set()
#     if rhs(graph, root, d) != d[root]:
#         cur.add(root)
#     while cur:
#         new_cur = []
#         for u in cur:
#             if rhs(graph, u, d) < d[u]:
#                 d[u] = rhs(graph, u, d)
#                 s.add(u)
#             elif d[u] < rhs(graph, u, d):
#                 d[u] = float('inf')
#                 s.add(u)
#             if u not in s:
#                 continue
#             for v in graph.successors(u):
#                 if v not in s and v not in cur:
#                     new_cur.append(v)
#         cur = new_cur
#
#     for v in s.union({root}):
#         if d[v] == float('inf'):
#             spt.remove_node(v)
#         else:
#             dists = [(d[u], u) for u in graph.predecessors(v)]
#             if not dists:
#                 raise Exception('у вершины с d != +inf обязан быть предок')
#             _, u = min(dists)
#             spt.add_edge(u, v)
#
#
# def update3(updated_edge, updated_graph: nx.DiGraph, spt: nx.DiGraph, d: List):
#     # в graph уже должны быть удалены/добавлены ребра, это уже пост обработка
#     (u, v) = updated_edge
#     if (u, v) in spt.edges:
#         if d[u] + 1 == d[v]:
#             d[v] = float('inf')
#             spt.remove_edge(u, v)
#         process_subtree(updated_graph, v, d, spt)
#     else:
#         # 1: удаляем ребро не из spt, тогда просто pass
#         # 2: добавляем новое ребро, тогда нужна проверка
#         if (u, v) in updated_graph.edges:
#             if d[u] + 1 < d[v]:
#                 process_subtree(updated_graph, v, d, spt)
