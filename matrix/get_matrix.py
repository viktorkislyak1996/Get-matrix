import logging
from asyncio import TimeoutError

import aiohttp
from aiohttp import ClientResponseError

from matrix.utils import prepare_matrix, traverse_matrix

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
                text_matrix = await response.text()
                return traverse_matrix(prepare_matrix(text_matrix))
    except TimeoutError as e:
        logger.error(f"Timeout error: {e}")
    except ClientResponseError as e:
        logger.error(f"Error while fetching matrix: {e}")
    return []
