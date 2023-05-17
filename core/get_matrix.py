import logging
from asyncio import TimeoutError

import aiohttp
from aiohttp import ClientResponseError

logger = logging.getLogger(__name__)


async def get_matrix(url: str) -> list[int]:
    """
    Receive a square matrix (NxN) from remote server and return it
    in the form of list[int]. This list contain the result
    of traversing the matrix in a spiral: counterclockwise,
    starting from the upper-left corner

    Args:
        url (str): The url of the remote server

    Returns:
        (list[int]): The traversed matrix
    """
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(
            timeout=timeout, raise_for_status=True
        ) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                matrix = await response.text()
                return traverse_matrix(matrix)
    except TimeoutError as e:
        logger.error(f"Timeout error: {e}")
    except ClientResponseError as e:
        logger.error(f"Error while fetching matrix: {e}")
    return []


def prepare_matrix(text_matrix: str) -> list[list[int]]:
    """
    Prepare the matrix from str format to a list of lists of integers

    Args:
        text_matrix (str): The matrix in a string format

    Returns:
        (list[list[int]]): The prepared matrix

    Raises:
        ValueError: If the matrix is not a square matrix
    """
    result = []
    list_of_rows = text_matrix.strip().split("\n")
    for row_str in list_of_rows:
        if row_str.startswith("|"):
            result.append([int(val) for val in row_str.strip("|").split("|")])

    if result and not all([len(result) == len(line) for line in result]):
        raise ValueError("The matrix is not square")
    return result


def traverse_matrix(matrix: str) -> list[int]:
    """
    Return a new list containing the result of traversing the matrix
    in a spiral: counterclockwise, starting from the upper left corner.

    Args:
        matrix (str): The matrix in a string format

    Returns:
        (list[int]): The traversed matrix
    """
    try:
        prepared_matrix = prepare_matrix(matrix)
    except ValueError as e:
        logger.error(e)
        return []

    end_row_idx = end_col_idx = len(prepared_matrix)
    start_row_idx = start_col_idx = 0
    result = []
    while start_row_idx < end_row_idx and start_col_idx < end_col_idx:
        # Traverse the first column from the remaining columns
        for i in range(start_row_idx, end_row_idx):
            result.append(prepared_matrix[i][start_col_idx])
        start_col_idx += 1

        # Traverse the last row from the remaining columns
        for j in range(start_col_idx, end_col_idx):
            result.append(prepared_matrix[end_row_idx - 1][j])
        end_row_idx -= 1

        # Traverse the last column from the remaining columns
        for i in range(end_row_idx - 1, start_row_idx - 1, -1):
            result.append(prepared_matrix[i][end_col_idx - 1])
        end_col_idx -= 1

        # Traverse the first row from the remaining columns
        for j in range(end_col_idx - 1, start_col_idx - 1, -1):
            result.append(prepared_matrix[start_row_idx][j])
        start_row_idx += 1

    return result
