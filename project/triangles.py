import pygraphblas as pgb


def count_triangles_per_each_vertex(adj_matrix: pgb.Matrix):
    """
    Подсчитывает количество треугольников для каждой вершины графа

    Parameters
    ----------
    adj_matrix: Matrix
       Матрица смежности

    Returns
    -------
    triangles_per_vertex: List[int]
        Список в i-й позиции которого указано количество треугольников для вершины i
    """
    _check_conditions(adj_matrix)
    m = adj_matrix.mxm(adj_matrix, cast=pgb.types.INT64, mask=adj_matrix)

    triangles_per_vertex = [0] * adj_matrix.ncols
    for i in range(adj_matrix.ncols):
        triangles_per_vertex[i] = m[i].reduce()
        triangles_per_vertex[i] //= 2

    return triangles_per_vertex


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

    diag = adj_matrix.vector_diag()
    for i in diag:
        if i != 0:
            raise ValueError("Граф не должен иметь петель")
    # for i in range(adj_matrix.ncols):
    #     if adj_matrix.get(i, i, 0) != 0:
    #         raise ValueError("Граф не должен иметь петель")
