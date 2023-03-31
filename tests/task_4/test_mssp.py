from typing import List

import pytest

from tests.utils import (
    read_data_from_json,
    create_matrix_from_two_lists,
)
from project.mssp import mssp


@pytest.mark.parametrize(
    "I, J, V, size, start_vertices, expected",
    read_data_from_json(
        "test_mssp",
        lambda data: (
            data["I"],
            data["J"],
            data["V"],
            data["size"],
            data["start_vertices"],
            [(d["vertex"], d["dists"]) for d in data["expected"]],
        ),
    ),
)
def test_mssp(I, J, V, size, start_vertices, expected):
    adj_matrix = create_matrix_from_two_lists(I, J, V, size)
    actual = mssp(adj_matrix, start_vertices)
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
def test_mssp_neg_cycle(I, J, V, size):
    adj_m = create_matrix_from_two_lists(I, J, V, size)
    with pytest.raises(ValueError):
        mssp(adj_m, [0, 1])
