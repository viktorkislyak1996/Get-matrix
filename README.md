# Technical specification

## Task condition

It is necessary to implement a Python library that retrieves a square matrix (NxN) from a remote server and returns it to the user in the form of a `List[int]`. This list should contain the result of traversing the resulting matrix in a spiral: counterclockwise, starting from the upper-left corner (see test case below).

Example of the original matrix

```
+-----+-----+-----+-----+
|  10 |  20 |  30 |  40 |
+-----+-----+-----+-----+
|  50 |  60 |  70 |  80 |
+-----+-----+-----+-----+
|  90 | 100 | 110 | 120 |
+-----+-----+-----+-----+
| 130 | 140 | 150 | 160 |
+-----+-----+-----+-----+
```

The matrix is guaranteed to contain non-negative integers. Formatting borders with other characters is not assumed.

## Requirements for implementation and design

- The library contains a function with the following interface:

    ```python
    async def get_matrix(url: str) -> List[int]:
        ...
    ```

- The function gets the URL for fetching the matrix from the server using the HTTP(S) protocol as a single argument.
- The function returns a list containing the result of traversing the resulting matrix in a spiral: counterclockwise, starting from the upper-left corner.
- Interaction with the server must be implemented asynchronously - via aiohttp, https or another component on asyncio.
- The library must correctly handle server and network errors. (5xx, Connection Timeout, Connection Refused, ...).
- In the future, the dimension of the matrix can be changed while maintaining the formatting. The library should maintain its operability on square matrices of a different dimension.
- The solution must be placed on one of the public git-hosting (GitHub, GitLab, Bitbucket). You can also send the solution as an archive (zip, tar). There is no need to upload the library to PyPI or other repositories.

## Checking the solution

- For self-checking, you can use the following test case:

    ```python
    SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'
    TRAVERSAL = [
        10, 50, 90, 130,
        140, 150, 160, 120,
        80, 40, 30, 20,
        60, 100, 110, 70,
    ]

    def test_get_matrix():
        assert asyncio.run(get_matrix(SOURCE_URL)) == TRAVERSAL
    ```
