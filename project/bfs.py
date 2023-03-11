from pygraphblas import Matrix, types, descriptor
from typing import List

__all__ = ["bfs"]


def bfs(adjacency_matrix: Matrix, start_vertex: int) -> List[int]:
    """
    Реализация алгоритма обхода ориентированного графа в ширину заданной вершины.
    Подсчитывает количество шагов за которое можно пройти из вершины до других.

    Parameters
    ----------
    adjacency_matrix: Matrix
        Матрица смежности данного графа
    start_vertex: int
        Вершина с которой начинаем обход в ширину

    Returns
    -------
    steps: List[int]
        Список с числом шагов от начальной вершины до других.
        Если вершина недостижима, то будет установлено значение -1.
    """

    _check_conditions(adjacency_matrix, start_vertex)

    res_matrix = Matrix.dense(
        types.INT64, nrows=1, ncols=adjacency_matrix.ncols, fill=-1
    )
    curr_front = Matrix.sparse(types.BOOL, nrows=1, ncols=adjacency_matrix.ncols)
    was_mask = Matrix.sparse(types.BOOL, nrows=1, ncols=adjacency_matrix.ncols)

    res_matrix[0, start_vertex] = 0
    curr_front[0, start_vertex] = True
    was_mask[0, start_vertex] = True

    step_number = 1
    prev_vals_number = -1
    while prev_vals_number != was_mask.nvals:
        prev_vals_number = was_mask.nvals
        curr_front.mxm(
            adjacency_matrix, mask=was_mask, out=curr_front, desc=descriptor.RC
        )
        was_mask.eadd(
            curr_front,
            curr_front.type.lxor_monoid,
            out=was_mask,
            desc=descriptor.R,
        )
        res_matrix.assign_scalar(step_number, mask=curr_front)
        step_number += 1

    return list(res_matrix[0].vals)


def _check_conditions(adjacency_matrix: Matrix, start_vertex: int):
    """
    Проверяет, что матрица смежности графа квадратная,
    сама матрица булева,
    номер стартовый вершины находится в диапазоне от 0 до числа вершин

    Parameters
    ----------
    adjacency_matrix: Matrix
       Матрица смежности
    start_vertex: int
       стартовая вершина
    """
    if not adjacency_matrix.square:
        raise ValueError("Матрица смежности должна быть квадратной")

    if adjacency_matrix.type != types.BOOL:
        raise ValueError(
            f"Неправильный тип матрицы: Действительный: {adjacency_matrix.type}, но Ожидался: BOOL"
        )

    if start_vertex < 0 or start_vertex >= adjacency_matrix.nrows:
        raise ValueError(
            f"Номер стартовый вершины должен быть между 0 и {adjacency_matrix.nrows - 1}"
        )
