from typing import List

import pytest

from tests.utils import read_data_from_json, create_matrix_from_list_of_lists
from project.triangles import count_triangles_per_each_vertex


@pytest.mark.parametrize(
    "matrix,  expected",
    read_data_from_json(
        "test_count_triangles_per_each_vertex",
        lambda data: (
            data["matrix"],
            data["expected"],
        ),
    ),
)
def test_count_triangles_per_each_vertex(matrix: List[List], expected: List[int]):
    adj_m = create_matrix_from_list_of_lists(matrix)
    actual = count_triangles_per_each_vertex(adj_m)
    assert actual == expected
