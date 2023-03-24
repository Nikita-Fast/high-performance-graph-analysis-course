import inspect
import json
import pathlib
import pygraphblas as pgb


def read_data_from_json(name, configurator):
    with pathlib.Path(inspect.stack()[1].filename) as f:
        parent = f.parent
    with open(parent / f"{name}.json") as f:
        data = json.load(f)
    return [configurator(block) for block in data[name]]


def create_matrix_from_two_lists(I, J, V, size) -> pgb.Matrix:
    m = pgb.Matrix.from_lists(I, J, V, nrows=size, ncols=size)
    print("успех")
    return m


def create_matrix_from_list_of_lists(lists):
    if lists == [[]]:
        raise ValueError("Матрица не может быть размера 0 на 0")
    n = len(lists)

    if not all(len(ls) == len(lists) for ls in lists):
        raise ValueError("Должна быть передана квадратная матрица")

    I, J = [], []
    for i in range(n):
        for j in range(n):
            if lists[i][j] != 0:
                I.append(i)
                J.append(j)
    nnz = len(I)
    V = [True] * nnz
    return pgb.Matrix.from_lists(I, J, V, nrows=n, ncols=n)
