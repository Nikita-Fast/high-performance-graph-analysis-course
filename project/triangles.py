from enum import Enum

import pygraphblas as pgb


class Algo(Enum):
    COHEN = 0
    SANDIA = 1


def count_triangles_in_graph(adj_matrix: pgb.Matrix, algo=Algo.SANDIA):
    """
    Подсчитывает количество треугольников в неориентированном графе

    Parameters
    ----------
    adj_matrix: Matrix
        Матрица смежности неориентированного графа
    algo: Algo
        Используемый для вычислений алгоритм

    Returns
    -------
    triangles_count: int
        Количество треугольников в графе
    """
    _check_conditions(adj_matrix)

    if algo == Algo.SANDIA:
        U = _extract_upper_triangle_matrix(adj_matrix)
        # Будь внимателен, здесь маска U!
        m = U.mxm(U, cast=pgb.types.INT64, mask=U)
        return sum(m.vals)

    elif algo == Algo.COHEN:
        U = _extract_upper_triangle_matrix(adj_matrix)
        L = _extract_lower_triangle_matrix(adj_matrix)
        # А здесь маска - вся матрица смежности!
        m = L.mxm(U, cast=pgb.types.INT64, mask=adj_matrix)
        return sum(m.vals) // 2
    else:
        raise ValueError("Неизвестный алгоритм подсчета треугольников")


def _extract_upper_triangle_matrix(adj_matrix: pgb.Matrix):
    U = pgb.Matrix.sparse(
        pgb.types.BOOL, nrows=adj_matrix.nrows, ncols=adj_matrix.ncols
    )
    for i, j, v in zip(adj_matrix.I, adj_matrix.J, adj_matrix.V):
        if i < j:
            U[i, j] = v
    return U


def _extract_lower_triangle_matrix(adj_matrix: pgb.Matrix):
    L = pgb.Matrix.sparse(
        pgb.types.BOOL, nrows=adj_matrix.nrows, ncols=adj_matrix.ncols
    )
    for i, j, v in zip(adj_matrix.I, adj_matrix.J, adj_matrix.V):
        if i > j:
            L[i, j] = v
    return L


def count_triangles_per_each_vertex(adj_matrix: pgb.Matrix):
    """
    Подсчитывает количество треугольников для каждой вершины неориентированного графа

    Parameters
    ----------
    adj_matrix: Matrix
       Матрица смежности неориентированного графа

    Returns
    -------
    triangles_per_vertex: List[int]
        Список в i-й позиции которого указано количество треугольников для вершины i
    """
    _check_conditions(adj_matrix)

    m = adj_matrix.mxm(adj_matrix, cast=pgb.types.INT64, mask=adj_matrix)

    # т.к. reduce_vector производит сложение по строкам, то транспонируем матрицу
    v = m.reduce_vector(desc=pgb.descriptor.T0)

    return [x // 2 for x in _sparse_to_dense_vector(v).vals]


def _sparse_to_dense_vector(v: pgb.Vector):
    fill = 0
    if v.nvals != 0:
        fill = v
    return v.dense(typ=pgb.types.INT64, size=v.size, fill=fill)


def _check_conditions(adj_matrix: pgb.Matrix):
    """
    Проверяет, что матрица смежности графа квадратная,
    сама матрица булева,
    матрица построена для неориентированного графа, в котором нет петель

    Parameters
    ----------
    adj_matrix: Matrix
       Матрица смежности
    """
    if not adj_matrix.square:
        raise ValueError("Матрица смежности должна быть квадратной")

    if adj_matrix.type != pgb.types.BOOL:
        raise ValueError(
            f"Неправильный тип матрицы: Действительный: {adj_matrix.type}, но Ожидался: BOOL"
        )

    if not adj_matrix.iseq(adj_matrix.transpose()):
        raise ValueError("Граф должен быть неориентированным")

    # todo Рустам, лучше так или закоментированный код чуть ниже будет предпочтительней?
    diag = adj_matrix.vector_diag()
    for i in diag:
        if i != 0:
            raise ValueError("Граф не должен иметь петель")
    # for i in range(adj_matrix.ncols):
    #     if adj_matrix.get(i, i, 0) != 0:
    #         raise ValueError("Граф не должен иметь петель")
