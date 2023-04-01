from typing import List, Tuple

import pygraphblas as pgb


def mssp(
    adj_matrix: pgb.Matrix, start_vertices: List[int]
) -> List[Tuple[int, List[int]]]:
    """
    Расширение алгоритма Бэлмана-Форда поиска кратчайших путей в графе для нескольких стартовых вершин

    Parameters
    ----------
    adj_matrix: Matrix
        Матрица смежности данного графа
    start_vertices: List[int]
        Стартовые вершины

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
    _check_conditions(adj_matrix, start_vertices)
    _prepare_matrix(adj_matrix)

    d = pgb.Matrix.sparse(
        pgb.types.FP64, nrows=len(start_vertices), ncols=adj_matrix.ncols
    )
    start_vertex_to_row_number = {v: i for i, v in enumerate(start_vertices)}
    for v, i in start_vertex_to_row_number.items():
        d[i, v] = 0

    for j in range(1, adj_matrix.ncols):
        d.mxm(adj_matrix, semiring=pgb.semiring.MIN_PLUS_FP64, out=d)

    # есть ли в графе отрицательные циклы?
    if d.isne(d.mxm(adj_matrix, semiring=pgb.semiring.MIN_PLUS_FP64)):
        raise ValueError("В графе есть циклы отрицательного веса!")
    else:
        return [
            (
                i,
                [
                    d.get(start_vertex_to_row_number[i], j, default=float("inf"))
                    for j in range(d.ncols)
                ],
            )
            for i in start_vertices
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


def _check_conditions(adjacency_matrix: pgb.Matrix, start_vertices: List[int]):
    """
    Проверяет, что матрица смежности графа квадратная,
    номер стартовый вершины находится в диапазоне от 0 до числа вершин

    Parameters
    ----------
    adjacency_matrix: Matrix
       Матрица смежности
    start_vertices: List[int]
       стартовые вершины
    """
    if not adjacency_matrix.square:
        raise ValueError("Матрица смежности должна быть квадратной")

    for start_vertex in start_vertices:
        if start_vertex < 0 or start_vertex >= adjacency_matrix.nrows:
            raise ValueError(
                f"Номер стартовой вершины должен быть между 0 и {adjacency_matrix.nrows - 1}"
            )
