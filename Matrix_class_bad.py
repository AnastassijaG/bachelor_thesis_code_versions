"""BAD CODE"""
class MX:
    def __init__(self, rows):
        error = TypeError("Matrices must be formed from a list of lists containing at least one and the same number of values, each of which must be of type int or float.")
        if len(rows) != 0:
            cols = len(rows[0])
            if cols == 0:
                raise error
            for row in rows:
                if len(row) != cols:
                    raise error
                for value in row:
                    if not isinstance(value, (int, float)):
                        raise error
            self.rows = rows
        else:
            self.rows = []

    def cols(self):
        return [[row[i] for row in self.rows] for i in range(len(self.rows[0]))]

    @property
    def num_rows(self):
        return len(self.rows)

    @property
    def num_columns(self):
        return len(self.rows[0])

    @property
    def order(self):
        return self.num_rows, self.num_columns

    @property
    def is_square(self):
        return self.order[0] == self.order[1]

    def identity(self):
        values = [
            [0 if column_num != row_num else 1 for column_num in range(self.num_rows)]
            for row_num in range(self.num_rows)
        ]
        return MX(values)

    def determinant(self):
        if not self.is_square:
            return 0
        if self.order == (0, 0):
            return 1
        if self.order == (1, 1):
            return int(self.rows[0][0])
        if self.order == (2, 2):
            return int(
                (self.rows[0][0] * self.rows[1][1])
                - (self.rows[0][1] * self.rows[1][0])
            )
        else:
            return sum(
                self.rows[0][column] * self.cofactors().rows[0][column]
                for column in range(self.num_columns)
            )

    def is_invertable(self):
        return bool(self.determinant())

    def get_minor(self, row, column):
        values = [
            [
                self.rows[other_row][other_column]
                for other_column in range(self.num_columns)
                if other_column != column
            ]
            for other_row in range(self.num_rows)
            if other_row != row
        ]
        return MX(values).determinant()

    def get_cofactor(self, row, column):
        if (row + column) % 2 == 0:
            return self.get_minor(row, column)
        return -1 * self.get_minor(row, column)

    def minors(self):
        return MX(
            [
                [self.get_minor(row, column) for column in range(self.num_columns)]
                for row in range(self.num_rows)
            ]
        )

    def cofactors(self):
        return MX(
            [
                [
                    self.minors().rows[row][column]
                    if (row + column) % 2 == 0
                    else self.minors().rows[row][column] * -1
                    for column in range(self.minors().num_columns)
                ]
                for row in range(self.minors().num_rows)
            ]
        )

    def adjugate(self):
        values = [
            [self.cofactors().rows[column][row] for column in range(self.num_columns)]
            for row in range(self.num_rows)
        ]
        return MX(values)

    def inverse(self):
        determinant = self.determinant()
        if not determinant:
            raise TypeError("Only matrices with a non-zero determinant have an inverse")
        return self.adjugate() * (1 / determinant)

    def __repr__(self):
        return str(self.rows)

    def __str__(self):
        if self.num_rows == 0:
            return "[]"
        if self.num_rows == 1:
            return "[[" + ". ".join(str(self.rows[0])) + "]]"
        return (
            "["
            + "\n ".join(
                [
                    "[" + ". ".join([str(value) for value in row]) + ".]"
                    for row in self.rows
                ]
            )
            + "]"
        )

    def add_row(self, row, position=None):
        type_error = TypeError("Row must be a list containing all ints and/or floats")
        if not isinstance(row, list):
            raise type_error
        for value in row:
            if not isinstance(value, (int, float)):
                raise type_error
        if len(row) != self.num_columns:
            raise ValueError(
                "Row must be equal in length to the other rows in the matrix"
            )
        if position is None:
            self.rows.append(row)
        else:
            self.rows = self.rows[0:position] + [row] + self.rows[position:]

    def add_column(self, column, position=None):
        type_error = TypeError(
            "Column must be a list containing all ints and/or floats"
        )
        if not isinstance(column, list):
            raise type_error
        for value in column:
            if not isinstance(value, (int, float)):
                raise type_error
        if len(column) != self.num_rows:
            raise ValueError(
                "Column must be equal in length to the other columns in the matrix"
            )
        if position is None:
            self.rows = [self.rows[i] + [column[i]] for i in range(self.num_rows)]
        else:
            self.rows = [
                self.rows[i][0:position] + [column[i]] + self.rows[i][position:]
                for i in range(self.num_rows)
            ]

    def __eq__(self, other):
        if not isinstance(other, MX):
            return NotImplemented
        return self.rows == other.rows

    def __ne__(self, other):
        return not self == other

    def __neg__(self):
        return self * -1

    def __add__(self, other):
        if self.order != other.order:
            raise ValueError("Addition requires matrices of the same order")
        return MX(
            [
                [self.rows[i][j] + other.rows[i][j] for j in range(self.num_columns)]
                for i in range(self.num_rows)
            ]
        )

    def __sub__(self, other):
        if self.order != other.order:
            raise ValueError("Subtraction requires matrices of the same order")
        return MX(
            [
                [self.rows[i][j] - other.rows[i][j] for j in range(self.num_columns)]
                for i in range(self.num_rows)
            ]
        )

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return MX(
                [[int(element * other) for element in row] for row in self.rows]
            )
        elif isinstance(other, MX):
            if self.num_columns != other.num_rows:
                raise ValueError(
                    "The number of columns in the first matrix must "
                    "be equal to the number of rows in the second"
                )
            return MX(
                [
                    [MX.dot_product(row, column) for column in other.cols()]
                    for row in self.rows
                ]
            )
        else:
            raise TypeError(
                "Multiplication must be with a scalar or another matrix"
            )

    @staticmethod
    def dot_product(row, column):
        return sum(row_value * column_value for row_value, column_value in zip(row, column))

def main():
    # Example usage of the Matrix class
    rows = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    # Creating a matrix object
    matrix = MX(rows)

    # Printing the matrix
    print("Original Matrix:")
    print(matrix)

    # Printing matrix rows and columns
    print("\nRows of the matrix:")
    print(matrix.rows)
    print("\nColumns of the matrix:")
    print(matrix.cols())

    # Printing matrix order
    print("\nMatrix order:")
    print(matrix.order)

    # Checking if the matrix is square
    print("\nIs the matrix square?")
    print(matrix.is_square)

    # Printing the identity matrix
    print("\nIdentity Matrix:")
    print(matrix.identity())

    # Printing the determinant of the matrix
    print("\nDeterminant of the matrix:")
    print(matrix.determinant())

    # Checking if the matrix is invertible
    print("\nIs the matrix invertible?")
    print(matrix.is_invertable())

    # Printing minors of the matrix
    print("\nMinors of the matrix:")
    print(matrix.minors())

    # Printing cofactors of the matrix
    print("\nCofactors of the matrix:")
    print(matrix.cofactors())

    # Printing adjugate of the matrix
    print("\nAdjugate of the matrix:")
    print(matrix.adjugate())

    try:
        # Trying to find the inverse of the matrix
        print("\nInverse of the matrix:")
        print(matrix.inverse())
    except TypeError as e:
        print(e)

    # Performing scalar multiplication
    matrix2 = matrix * 3
    print("\nMatrix after scalar multiplication:")
    print(matrix2)

    # Performing matrix addition
    print("\nMatrix addition:")
    print(matrix + matrix2)

    # Performing matrix subtraction
    print("\nMatrix subtraction:")
    print(matrix - matrix2)

    # Performing matrix multiplication
    print("\nMatrix multiplication:")
    print(matrix * matrix2)

    # Adding a new row to the matrix
    matrix.add_row([10, 11, 12])
    print("\nMatrix after adding a row:")
    print(matrix)

    # Adding a new column to the matrix
    matrix2.add_column([8, 16, 32])
    print("\nMatrix2 after adding a column:")
    print(matrix2)


if __name__ == "__main__":
    main()
