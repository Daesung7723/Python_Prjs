from __future__ import annotations
from src.tetromino import Tetromino


class Board:
    WIDTH  = 10
    HEIGHT = 20

    def __init__(self) -> None:
        self._grid: list[list[int]] = self._empty_grid()

    def _empty_grid(self) -> list[list[int]]:
        return [[0] * self.WIDTH for _ in range(self.HEIGHT)]

    def get(self, x: int, y: int) -> int:
        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
            return self._grid[y][x]
        return 0

    def is_valid(self, piece: Tetromino, dx: int = 0, dy: int = 0) -> bool:
        for bx, by in piece.get_cells():
            nx, ny = bx + dx, by + dy
            if nx < 0 or nx >= self.WIDTH:
                return False
            if ny >= self.HEIGHT:
                return False
            # y < 0 허용: 생성 직후 보드 위에 있는 상태
            if ny >= 0 and self._grid[ny][nx] != 0:
                return False
        return True

    def lock(self, piece: Tetromino) -> None:
        for bx, by in piece.get_cells():
            if 0 <= by < self.HEIGHT and 0 <= bx < self.WIDTH:
                self._grid[by][bx] = piece.type.value

    def clear_lines(self) -> int:
        full = [
            y for y in range(self.HEIGHT)
            if all(self._grid[y][x] != 0 for x in range(self.WIDTH))
        ]
        for y in sorted(full, reverse=True):
            self._grid.pop(y)
        for _ in full:
            self._grid.insert(0, [0] * self.WIDTH)
        return len(full)

    def ghost_y(self, piece: Tetromino) -> int:
        drop = 0
        while self.is_valid(piece, dx=0, dy=drop + 1):
            drop += 1
        return piece.y + drop

    def is_game_over(self) -> bool:
        return any(self._grid[0][x] != 0 for x in range(self.WIDTH))

    def reset(self) -> None:
        self._grid = self._empty_grid()
