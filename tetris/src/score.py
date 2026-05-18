from __future__ import annotations


class ScoreManager:
    _SCORE_TABLE   = {1: 100, 2: 300, 3: 500, 4: 800}
    _LINES_PER_LEVEL = 10

    def __init__(self) -> None:
        self.score = 0
        self.level = 1
        self.lines = 0

    def add_clear(self, n: int) -> None:
        if n <= 0:
            return
        self.score += self._SCORE_TABLE.get(n, 800) * self.level
        self.lines += n
        self.level  = min(self.lines // self._LINES_PER_LEVEL + 1, 15)

    def add_soft_drop(self, n: int = 1) -> None:
        self.score += n

    def add_hard_drop(self, n: int) -> None:
        self.score += n * 2

    def fall_interval(self) -> float:
        lvl = min(self.level, 15)
        return max((0.8 - (lvl - 1) * 0.007) ** (lvl - 1), 0.020)

    def reset(self) -> None:
        self.score = 0
        self.level = 1
        self.lines = 0
