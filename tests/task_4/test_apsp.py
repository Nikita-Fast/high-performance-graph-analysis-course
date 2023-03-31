from project.apsp import floyd_warshall
from typing import List

import pytest

from tests.utils import (
    read_data_from_json,
    create_matrix_from_two_lists,
)


@pytest.mark.parametrize(
    "I, J, V, size, expected",
    read_data_from_json(
        "test_apsp",
        lambda data: (
            data["I"],
            data["J"],
            data["V"],
            data["size"],
            [(d["vertex"], d["dists"]) for d in data["expected"]],
        ),
    ),
)
def test_apsp(I, J, V, size, expected):
    adj_matrix = create_matrix_from_two_lists(I, J, V, size)
    actual = floyd_warshall(adj_matrix)
    assert actual == expected


@pytest.mark.parametrize(
    "I, J, V, size",
    read_data_from_json(
        "test_neg_cycle",
        lambda data: (
            data["I"],
            data["J"],
            data["V"],
            data["size"],
        ),
    ),
)
def test_apsp_neg_cycle(I, J, V, size):
    adj_m = create_matrix_from_two_lists(I, J, V, size)
    with pytest.raises(ValueError):
        floyd_warshall(adj_m)
