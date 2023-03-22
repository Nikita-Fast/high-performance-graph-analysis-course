import pygraphblas as pgb
from typing import List, Collection, Tuple

__all__ = ["msbfs"]


def msbfs(
    adj_matrix: pgb.Matrix, start_vertices: Collection[int]
) -> List[Tuple[int, List[int]]]:
    """
    Реализация BFS от нескольких стартовых вершин для ориентированного графа

    Parameters
    ----------
    adj_matrix: Matrix
        Матрица смежности данного графа
    start_vertices: Collection[int]
        Вершины с которой начинаем обход в ширину

    Returns
    -------
    Список пар вида (start_vertex, parents) где каждой стартовой вершине сопоставляется
    n родительских вершин. При наличии нескольких возможных родительских вершин
    выбираем вершину с меньшим номером. Стартовые вершины в данном списке будут иметь значение -1, а
    недостижимые вершины будут иметь значение -2.
    """
    _check_conditions_msbfs(adj_matrix, start_vertices)

    parents = pgb.Matrix.sparse(
        pgb.INT64, nrows=len(start_vertices), ncols=adj_matrix.ncols
    )
    curr_front = pgb.Matrix.sparse(
        pgb.INT64, nrows=len(start_vertices), ncols=adj_matrix.ncols
    )
    for row, start in enumerate(start_vertices):
        parents[row, start] = -1
        curr_front[row, start] = start

    while curr_front.nvals > 0:
        curr_front.mxm(
            other=adj_matrix,
            out=curr_front,
            semiring=pgb.INT64.MIN_FIRST,
            mask=parents.S,
            desc=pgb.descriptor.RC,
        )
        parents.assign(value=curr_front, mask=curr_front.S)
        curr_front.apply(op=pgb.INT64.POSITIONJ, out=curr_front, mask=curr_front.S)

    return [
        (start, [parents.get(row, col, default=-2) for col in range(adj_matrix.ncols)])
        for row, start in enumerate(start_vertices)
    ]


def _check_conditions_msbfs(
    adjacency_matrix: pgb.Matrix, start_vertices: Collection[int]
):
    """
    Проверяет, что матрица смежности графа квадратная,
    сама матрица булева,
    номер стартовых вершин находится в диапазоне от 0 до числа вершин

    Parameters
    ----------
    adjacency_matrix: Matrix
       Матрица смежности
    start_vertices: Collection[int]
       стартовые вершины
    """
    if not adjacency_matrix.square:
        raise ValueError("Матрица смежности должна быть квадратной")

    if adjacency_matrix.type != pgb.types.BOOL:
        raise ValueError(
            f"Неправильный тип матрицы: Действительный: {adjacency_matrix.type}, но Ожидался: BOOL"
        )

    for start_vertex in start_vertices:
        if start_vertex < 0 or start_vertex >= adjacency_matrix.nrows:
            raise ValueError(
                f"Номер стартовой вершины должен быть между 0 и {adjacency_matrix.nrows - 1}"
            )
