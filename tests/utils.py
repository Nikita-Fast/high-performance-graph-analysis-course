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
