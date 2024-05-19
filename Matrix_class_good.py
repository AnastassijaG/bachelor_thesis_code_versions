"""GOOD CODE"""

from __future__ import annotations

class Matrix:
    def __init__(self, rows: list[list[int | float]]):
        self._validate_rows(rows)
        self._rows = rows

    @staticmethod
    def _validate_rows(rows):
        if not rows:
            return
        num_columns = len(rows[0])
        if num_columns == 0 or not all(len(row) == num_columns for row in rows):
            raise ValueError("Matrix rows must have the same length and contain int or float values")

    @property
    def rows(self) -> list[list[int | float]]:
        return self._rows

    def columns(self) -> list[list[int | float]]:
        return [list(column) for column in zip(*self._rows)]

    @property
    def order(self) -> tuple[int, int]:
        return len(self._rows), len(self._rows[0])

    @property
    def is_square(self) -> bool:
        return self.order[0] == self.order[1]

    def identity(self) -> 'Matrix':
        if not self.is_square:
            raise ValueError("Identity matrix can only be generated for square matrices")
        n = self.order[0]
        return Matrix([[1 if i == j else 0 for j in range(n)] for i in range(n)])

    def determinant(self) -> int | float | None:
        if not self.is_square:
            return None
        n = self.order[0]
        if n == 1:
            return self._rows[0][0]
        if n == 2:
            return self._rows[0][0] * self._rows[1][1] - self._rows[0][1] * self._rows[1][0]
        det = 0
        for j in range(n):
            det += self._rows[0][j] * self._get_cofactor(0, j)
        return det

    def _get_minor(self, row: int, col: int) -> 'Matrix':
        return Matrix([row[:col] + row[col + 1:] for row in (self._rows[:row] + self._rows[row + 1:])])

    def _get_cofactor(self, row: int, col: int) -> int | float:
        minor = self._get_minor(row, col)
        sign = -1 if (row + col) % 2 == 1 else 1
        return sign * minor.determinant()

    def inverse(self) -> 'Matrix':
        det = self.determinant()
        if det == 0:
            return None
        n = self.order[0]
        adjugate = Matrix([[self._get_cofactor(i, j) for j in range(n)] for i in range(n)])
        return adjugate.transpose() * (1 / det)

    def transpose(self) -> 'Matrix':
        return Matrix(list(zip(*self._rows)))

    def __repr__(self) -> str:
        return str(self._rows)

    def __str__(self) -> str:
        if not self._rows:
            return "[]"
        if len(self._rows) == 1:
            return "[[" + ". ".join(map(str, self._rows[0])) + "]]"
        return (
            "["
            + "\n ".join(
                [
                    "[" + ". ".join(map(str, row)) + ".]"
                    for row in self._rows
                ]
            )
            + "]"
        )

if __name__ == "__main__":
    # Initial test matrix
    rows = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    matrix = Matrix(rows)

    print("Original Matrix:")
    print(matrix)

    print("Matrix columns:")
    print(matrix.columns())

    print("Matrix order:")
    print(matrix.order)

    print("Is matrix square?")
    print(matrix.is_square)

    print("Identity matrix:")
    try:
        identity = matrix.identity()
        print(identity)
    except ValueError as e:
        print(e)

    print("Determinant:")
    print(matrix.determinant())

    print("Transpose:")
    print(matrix.transpose())

    print("Inverse:")
    try:
        inverse = matrix.inverse()
        print(inverse)
    except ValueError as e:
        print(e)