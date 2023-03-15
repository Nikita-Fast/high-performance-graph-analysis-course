from pygraphblas import Matrix, types, descriptor, Vector
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

    res_vector = Vector.sparse(types.INT64, size=adjacency_matrix.ncols)
    curr_front = Vector.sparse(types.BOOL, size=adjacency_matrix.ncols)

    res_vector[start_vertex] = 0
    curr_front[start_vertex] = True

    step_number = 1
    while curr_front.nvals != 0:
        curr_front.vxm(
            adjacency_matrix, mask=res_vector.S, out=curr_front, desc=descriptor.RC
        )
        res_vector.assign_scalar(step_number, mask=curr_front)
        step_number += 1

    res_vector.assign_scalar(-1, mask=res_vector.S, desc=descriptor.C)
    return list(res_vector.vals)


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
