import logging

logger = logging.getLogger(__name__)


def traverse_matrix(matrix: list[list[int]]) -> list[int]:
    """
    Return a new list containing the result of traversing the matrix
    in a spiral: counterclockwise, starting from the upper left corner.

    Args:
        matrix (list[list[int]]): The original matrix

    Returns:
        (list[int]): The traversed matrix
    """
    end_row_idx = end_col_idx = len(matrix)
    start_row_idx = start_col_idx = 0
    result = []
    while start_row_idx < end_row_idx and start_col_idx < end_col_idx:
        # Traverse the first column from the remaining columns
        for i in range(start_row_idx, end_row_idx):
            result.append(matrix[i][start_col_idx])
        start_col_idx += 1

        # Traverse the last row from the remaining columns
        for j in range(start_col_idx, end_col_idx):
            result.append(matrix[end_row_idx - 1][j])
        end_row_idx -= 1

        # Traverse the last column from the remaining columns
        for i in range(end_row_idx - 1, start_row_idx - 1, -1):
            result.append(matrix[i][end_col_idx - 1])
        end_col_idx -= 1

        # Traverse the first row from the remaining columns
        for j in range(end_col_idx - 1, start_col_idx - 1, -1):
            result.append(matrix[start_row_idx][j])
        start_row_idx += 1
    return result


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
    try:
        result = []
        list_of_rows = text_matrix.strip().split("\n")
        for row_str in list_of_rows:
            if row_str.startswith("|"):
                result.append([int(val) for val in row_str.strip("|").split("|")])

        if result and not all([len(result) == len(line) for line in result]):
            raise ValueError("The matrix is not square")
    except ValueError as e:
        logger.error(e)
        return []
    return result
