from typing import Optional, Sequence

import aiohttp


async def get_matrix(url: str) -> Sequence[Optional[int]]:
    """
    Receive a square matrix (NxN) from remote server and return it
    if the form of list[int]. This list contain the result
    of traversing the matrix in a spiral: counterclockwise,
    starting from the upper-left corner

    Args:
        url (str): The url of the remote server

    Returns:
        (Sequence[Optional[int]]): The traversed matrix
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            matrix = await response.text()
            return traverse_matrix(matrix)


def traverse_matrix(matrix: str | None) -> Sequence[Optional[int]]:
    """
    Return a new list containing the result of traversing the matrix
    in a spiral: counterclockwise, starting from the upper left corner.

    Args:
        matrix (str | None): The matrix in a string format

    Returns:
        (Sequence[Optional[int]]): The traversed matrix
    """
    if not matrix:
        return []

    prepared_matrix = prepare_matrix(matrix)

    end_row_idx = end_col_idx = len(prepared_matrix)
    start_row_idx, start_col_idx = 0, 0
    result = []
    while start_row_idx < end_row_idx and start_col_idx < end_col_idx:
        # Traverse the first column from the remaining columns
        for i in range(start_row_idx, end_row_idx):
            el = prepared_matrix[i][start_col_idx]
            result.append(el)
        start_col_idx += 1

        # Traverse the last row from the remaining columns
        for j in range(start_col_idx, end_col_idx):
            el = prepared_matrix[end_row_idx - 1][j]
            result.append(el)
        end_row_idx -= 1

        # Traverse the last column from the remaining columns
        for i in range(end_row_idx - 1, start_row_idx - 1, -1):
            el = prepared_matrix[i][end_col_idx - 1]
            result.append(el)
        end_col_idx -= 1

        # Traverse the first row from the remaining columns
        for j in range(end_col_idx - 1, start_col_idx - 1, -1):
            el = prepared_matrix[start_row_idx][j]
            result.append(el)
        start_row_idx += 1

    return result


def prepare_matrix(matrix: str) -> list[list[int]]:
    """
    Preparing the matrix to a list of lists of integers

    Args:
        matrix (str): The matrix in a string format

    Returns:
        (list[list[int]]): The prepared matrix
    """
    result = []
    list_of_rows = matrix.split("\n")
    for el in list_of_rows:
        if el.startswith("|"):
            list_of_strings = el.strip("|").split("|")
            result.append(list(map(int, list_of_strings)))
    return result
