import pygraphblas as pgb
import pytest

from project import msbfs

from tests.utils import read_data_from_json, create_matrix_from_two_lists


@pytest.fixture(params=[pgb.INT64, pgb.INT32, pgb.FC64, pgb.UINT8])
def pgb_types(request):
    return request.param


@pytest.fixture(params=[(2, 3), (3, 2), (1, 5), (5, 1)])
def matrix_size(request):
    return request.param


def test_non_square_adj_matrix(matrix_size):
    adj_matrix = pgb.Matrix.dense(pgb.BOOL, nrows=matrix_size[0], ncols=matrix_size[1])
    with pytest.raises(ValueError):
        msbfs(adj_matrix, [0])


def test_wrong_matrix_type(pgb_types):
    adjacency_matrix = pgb.Matrix.dense(pgb_types, nrows=3, ncols=3)
    with pytest.raises(ValueError):
        msbfs(adjacency_matrix, [0])


@pytest.mark.parametrize(
    "start_vertices",
    read_data_from_json(
        "test_msbfs_wrong_start_vertices",
        lambda data: (data["start_vertices"]),
    ),
)
def test_wrong_start_vertices(start_vertices):
    adjacency_matrix = pgb.Matrix.dense(pgb.BOOL, nrows=3, ncols=3)
    with pytest.raises(ValueError):
        msbfs(adjacency_matrix, start_vertices)


@pytest.mark.parametrize(
    "I, J, V, size, start_vertices, expected",
    read_data_from_json(
        "test_msbfs",
        lambda data: (
            data["I"],
            data["J"],
            data["V"],
            data["size"],
            data["start_vertices"],
            [(p["start_vertex"], p["parents"]) for p in data["expected"]],
        ),
    ),
)
def test_msbfs_method(I, J, V, size, start_vertices, expected):
    adj_m = create_matrix_from_two_lists(I, J, V, size)
    actual = msbfs(adj_m, start_vertices)
    assert actual == expected
