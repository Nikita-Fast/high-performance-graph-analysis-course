from typing import List, Tuple

import pygraphblas as pgb
import numpy as np


def floyd_warshall(adj_matrix: pgb.Matrix) -> List[Tuple[int, List[int]]]:
    """
    Алгоритм Флойда–Уоршелла поиска длин кратчайших путей между всеми парами вершин во
    взвешенном ориентированном графе.

    Parameters
    ----------
    adj_matrix: Matrix
        Матрица смежности данного графа

    Raises
    ------
    ValueError
        Если в графе есть цикл с отрицательным весом

    Returns
    -------
    distances: List[Tuple[int, List[int]]]
        Массив пар: вершина, и массив, где для каждой вершины указано расстояние до неё из указанной.
        Если вершина не достижима, то значение соответствующей ячейки равно -1.
    """
    # todo надо просто посчитать транзитивное замыкание матрицы над min_plus полукольцом?
    _check_conditions(adj_matrix)
    _prepare_matrix(adj_matrix)

    old_nvals = -1
    while adj_matrix.nvals != old_nvals:
        old_nvals = adj_matrix.nvals
        adj_matrix.mxm(
            adj_matrix,
            semiring=adj_matrix.type.min_plus,
            out=adj_matrix,
            accum=adj_matrix.type.min,
        )

    for i in range(adj_matrix.nrows):
        if adj_matrix[i, i] < 0:
            raise ValueError("В графе есть цикл с отрицательным весом")

    return [
        (
            i,
            [
                adj_matrix.get(i, j, default=float("inf"))
                for j in range(adj_matrix.ncols)
            ],
        )
        for i in range(adj_matrix.nrows)
    ]


def _prepare_matrix(adj_matrix: pgb.Matrix):
    """
    Заполняет главную диагональ матрицы нулями

    Parameters
    ----------
    adj_matrix: Matrix
       Матрица смежности
    """
    for i in range(adj_matrix.ncols):
        adj_matrix[i, i] = 0


def _check_conditions(adjacency_matrix: pgb.Matrix):
    """
    Проверяет, что матрица смежности графа квадратная

    Parameters
    ----------
    adjacency_matrix: Matrix
       Матрица смежности
    """
    if not adjacency_matrix.square:
        raise ValueError("Матрица смежности должна быть квадратной")
