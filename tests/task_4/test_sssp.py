from typing import List

import pytest

from tests.utils import (
    read_data_from_json,
    create_matrix_from_list_of_lists,
    create_matrix_from_two_lists,
)
from project.sssp import bellman_ford


@pytest.mark.parametrize(
    "I, J, V, size, start_vertex, expected",
    read_data_from_json(
        "test_sssp",
        lambda data: (
            data["I"],
            data["J"],
            data["V"],
            data["size"],
            data["start_vertex"],
            data["expected"],
        ),
    ),
)
def test_bellman_ford(I, J, V, size: int, start_vertex: int, expected: List[int]):
    adj_m = create_matrix_from_two_lists(I, J, V, size)
    actual = bellman_ford(adj_m, start_vertex)
    assert actual == expected


@pytest.mark.parametrize(
    "I, J, V, size",
    read_data_from_json(
        "test_sssp_neg_cycle",
        lambda data: (
            data["I"],
            data["J"],
            data["V"],
            data["size"],
        ),
    ),
)
def test_bellman_ford_neg_cycle(I, J, V, size: int):
    adj_m = create_matrix_from_two_lists(I, J, V, size)
    with pytest.raises(ValueError):
        bellman_ford(adj_m, start_vertex=0)
