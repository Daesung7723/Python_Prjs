from __future__ import annotations
import random
from enum import Enum


class TetrominoType(Enum):
    I = 1
    O = 2
    T = 3
    S = 4
    Z = 5
    J = 6
    L = 7


SHAPES: dict[TetrominoType, list[list[list[int]]]] = {
    TetrominoType.I: [
        [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
    ],
    TetrominoType.O: [
        [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    ],
    TetrominoType.T: [
        [[0, 1, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
    ],
    TetrominoType.S: [
        [[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],
    ],
    TetrominoType.Z: [
        [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]],
    ],
    TetrominoType.J: [
        [[1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]],
    ],
    TetrominoType.L: [
        [[0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 0], [0, 0, 0, 0]],
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
    ],
}

COLORS: dict[TetrominoType, tuple[int, int, int]] = {
    TetrominoType.I: (0,   240, 240),
    TetrominoType.O: (240, 240, 0),
    TetrominoType.T: (160, 0,   240),
    TetrominoType.S: (0,   240, 0),
    TetrominoType.Z: (240, 0,   0),
    TetrominoType.J: (0,   0,   240),
    TetrominoType.L: (240, 160, 0),
}


class Tetromino:
    def __init__(self, t_type: TetrominoType, x: int = 3, y: int = 0) -> None:
        self.type     = t_type
        self.x        = x
        self.y        = y
        self.rotation = 0
        self.color    = COLORS[t_type]

    @property
    def shape(self) -> list[list[int]]:
        return SHAPES[self.type][self.rotation]

    def get_cells(self) -> list[tuple[int, int]]:
        cells = []
        for row in range(4):
            for col in range(4):
                if self.shape[row][col]:
                    cells.append((self.x + col, self.y + row))
        return cells

    def rotate_cw(self) -> None:
        self.rotation = (self.rotation + 1) % 4

    def rotate_ccw(self) -> None:
        self.rotation = (self.rotation - 1) % 4

    def copy(self) -> Tetromino:
        t = Tetromino(self.type, self.x, self.y)
        t.rotation = self.rotation
        return t


class TetrominoFactory:
    @staticmethod
    def create(t_type: TetrominoType) -> Tetromino:
        return Tetromino(t_type)

    @staticmethod
    def random() -> Tetromino:
        return Tetromino(random.choice(list(TetrominoType)))
