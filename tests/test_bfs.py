import pygraphblas as pgb
import pytest

from project import bfs

from tests.utils import read_data_from_json, create_matrix_from_two_lists


@pytest.fixture(params=[pgb.INT64, pgb.INT32, pgb.FC64, pgb.UINT8])
def pgb_types(request):
    return request.param


def test_non_square_adj_matrix():
    adj_matrix = pgb.Matrix.dense(pgb.BOOL, nrows=2, ncols=5)
    with pytest.raises(ValueError):
        bfs(adj_matrix, 0)


def test_wrong_matrix_type(pgb_types):
    adjacency_matrix = pgb.Matrix.dense(pgb_types, nrows=3, ncols=3)
    with pytest.raises(ValueError):
        bfs(adjacency_matrix, 0)


def test_wrong_start_vertex():
    adjacency_matrix = pgb.Matrix.dense(pgb.BOOL, nrows=3, ncols=3)
    with pytest.raises(ValueError):
        bfs(adjacency_matrix, -1)


# @pytest.mark.parametrize(
#     "adj_m, start, expected",
#     read_data_from_json(
#         "test_bfs",
#         lambda data: (
#             create_matrix_from_two_lists(
#                 I=data["I"],
#                 J=data["J"],
#                 V=data["V"],
#                 size=data["size"],
#             ),
#             data["start"],
#             data["expected"],
#         ),
#     ),
# )
# def test_bfs_method(adj_m: pgb.Matrix, start: int, expected):
#     actual = bfs(adj_m, start)
#     assert actual == expected


@pytest.mark.parametrize(
    "I, J, V, size, start, expected",
    read_data_from_json(
        "test_bfs",
        lambda data: (
            data["I"],
            data["J"],
            data["V"],
            data["size"],
            data["start"],
            data["expected"],
        ),
    ),
)
def test_bfs_method(I, J, V, size, start, expected):
    print("test_bfs_method")
    adj_m = create_matrix_from_two_lists(I, J, V, size)
    actual = bfs(adj_m, start)
    assert actual == expected
