import pygraphblas as pgb


def bellman_ford(adj_matrix: pgb.Matrix, start_vertex: int):
    """
    Алгоритм Бэлмана-Форда поиска кратчайших путей в графе из единственной стартовой вершины.

    Parameters
    ----------
    adj_matrix: Matrix
        Матрица смежности данного графа
    start_vertex: int
        Вершина с которой начинаем обход в ширину

    Raises
    ------
    ValueError
        Если в графе есть цикл с отрицательным весом

    Returns
    -------
    distances: List[int]
        Список, где для каждой вершины указано расстояние до неё от указанной стартовой вершины.
    Если вершина не достижима, то значение соответствующей ячейки равно -1.
    """
    _check_conditions(adj_matrix, start_vertex)
    _prepare_matrix(adj_matrix)

    d = pgb.Vector.sparse(pgb.types.FP64, size=adj_matrix.ncols)
    d[start_vertex] = 0
    for j in range(1, adj_matrix.ncols):
        d.vxm(adj_matrix, semiring=pgb.semiring.MIN_PLUS_FP64, out=d)

    # есть ли в графе отрицательные циклы?
    if d.isne(d.vxm(adj_matrix, semiring=pgb.semiring.MIN_PLUS_FP64)):
        raise ValueError("В графе есть циклы отрицательного веса!")
    else:
        return [d.get(i, default=float("inf")) for i in range(adj_matrix.ncols)]


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


def _check_conditions(adjacency_matrix: pgb.Matrix, start_vertex: int):
    """
    Проверяет, что матрица смежности графа квадратная,
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

    if start_vertex < 0 or start_vertex >= adjacency_matrix.nrows:
        raise ValueError(
            f"Номер стартовый вершины должен быть между 0 и {adjacency_matrix.nrows - 1}"
        )
