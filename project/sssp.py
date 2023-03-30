import pygraphblas as pgb


def bellman_ford(adj_matrix: pgb.Matrix, start_vertex: int):
    """
    Матрица не булева!
    :param adj_matrix:
    :param start_vertex:
    :return:
    """
    # _check_conditions(adj_matrix, start_vertex)
    # todo матрица не булева
    # todo есть ли отрицательные цикла?

    # todo на диагонали в матрице должны быть нули
    for i in range(adj_matrix.ncols):
        adj_matrix[i, i] = 0

    d = pgb.Vector.sparse(pgb.types.FP64, size=adj_matrix.ncols)
    d[start_vertex] = 0
    for j in range(1, adj_matrix.ncols):
        d.vxm(adj_matrix, semiring=pgb.semiring.MIN_PLUS_FP64, out=d)
        # print(j, [d.get(i, default=-1) for i in range(adj_matrix.ncols)])

    return [d.get(i, default=-1) for i in range(adj_matrix.ncols)]


def _check_conditions(adjacency_matrix: pgb.Matrix, start_vertex: int):
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

    if adjacency_matrix.type != pgb.types.BOOL:
        raise ValueError(
            f"Неправильный тип матрицы: Действительный: {adjacency_matrix.type}, но Ожидался: BOOL"
        )

    if start_vertex < 0 or start_vertex >= adjacency_matrix.nrows:
        raise ValueError(
            f"Номер стартовый вершины должен быть между 0 и {adjacency_matrix.nrows - 1}"
        )
