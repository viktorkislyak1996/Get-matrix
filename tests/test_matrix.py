import asyncio
from unittest.mock import MagicMock, patch

import aiohttp
import pytest

from matrix.get_matrix import get_matrix
from matrix.utils import prepare_matrix, traverse_matrix

SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/' \
             'python-trainee-assignment/main/matrix.txt'

TRAVERSAL_MATRIX = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]

PREPARED_MATRIX = [
    [10, 20, 30, 40],
    [50, 60, 70, 80],
    [90, 100, 110, 120],
    [130, 140, 150, 160]
]

TEXT_MATRIX = "+-----+-----+-----+-----+\n" \
              "|  10 |  20 |  30 |  40 |\n" \
              "+-----+-----+-----+-----+\n" \
              "|  50 |  60 |  70 |  80 |\n" \
              "+-----+-----+-----+-----+\n" \
              "|  90 | 100 | 110 | 120 |\n" \
              "+-----+-----+-----+-----+\n" \
              "| 130 | 140 | 150 | 160 |\n" \
              "+-----+-----+-----+-----+"


def test_get_matrix():
    matrix = asyncio.run(get_matrix(SOURCE_URL))
    assert matrix == TRAVERSAL_MATRIX


@pytest.mark.parametrize('input_data, expected', [
    (TEXT_MATRIX, PREPARED_MATRIX),
    ('', []),
    ("+-----+-----+\n|  10 |  20 |", []),
    (
        "+-----+-----+\n|  10 |  20 |\n+-----+-----+\n|  30 |  40 |",
        [[10, 20], [30, 40]]
    ),
    ('test case', [])
])
def test_prepare_matrix(input_data, expected):
    assert prepare_matrix(input_data) == expected


@pytest.mark.parametrize('input_data, expected', [
    (PREPARED_MATRIX, TRAVERSAL_MATRIX),
    ([], []),
    ([[10, 20], [30, 40]], [10, 30, 40, 20])
])
def test_traverse_matrix(input_data, expected):
    assert traverse_matrix(input_data) == expected


@pytest.mark.asyncio
async def test_get_matrix_success():
    mock_value = "+-----+-----+\n|  10 |  20 |\n+-----+-----+\n|  30 |  40 |"
    mock = aiohttp.ClientSession
    mock.get = MagicMock()
    mock.get.return_value.__aenter__.return_value.status = 200
    mock.get.return_value.__aenter__.return_value.text.return_value = mock_value
    result = await get_matrix(SOURCE_URL)
    assert result == [10, 30, 40, 20]


@pytest.mark.asyncio
async def test_get_matrix_timeout():
    with patch("aiohttp.ClientSession.get", side_effect=asyncio.TimeoutError):
        result = await get_matrix(SOURCE_URL)
        assert result == []
