import math


class Transforms:
    @staticmethod
    def identity():
        """Retorna a matriz identidade 3x3."""
        return [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]

    @staticmethod
    def translation(dx, dy):
        return [
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ]

    @staticmethod
    def scale(sx, sy):
        return [
            [1 * sx, 0, 0],
            [0, 1 * sy, 0],
            [0, 0, 1]
        ]

    @staticmethod
    def rotation(angle_degrees):
        rad = math.radians(angle_degrees)
        return [
            [math.cos(rad), -math.sin(rad), 0],
            [math.sin(rad),  math.cos(rad), 0],
            [0, 0, 1]
        ]

    @staticmethod
    def multiply(A, B):
        """Multiplicação de matrizes 3x3."""
        C = [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
        for i in range(3):
            for j in range(3):
                C[i][j] = sum(A[i][k] * B[k][j] for k in range(3))
        return C

    @staticmethod
    def apply(matrix, point):
        """Aplica a matriz a um ponto (x, y)."""
        x, y = point
        # Coordenada homogênea [x, y, 1]
        new_x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * 1
        new_y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * 1
        return (new_x, new_y)
