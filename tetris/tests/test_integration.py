"""
통합 테스트: Board + Tetromino + ScoreManager 연동 검증
(pygame 렌더링 없이 게임 로직만 테스트)
"""
import pytest
from src.board import Board
from src.tetromino import Tetromino, TetrominoType, TetrominoFactory
from src.score import ScoreManager


def drop_to_bottom(board: Board, piece: Tetromino) -> int:
    """piece를 바닥까지 내리고 낙하 칸 수 반환."""
    distance = 0
    while board.is_valid(piece, dy=1):
        piece.y += 1
        distance += 1
    return distance


def place_piece(board: Board, piece: Tetromino, x: int, y: int | None = None):
    """지정 위치에 블록을 놓고 보드에 고정."""
    piece.x = x
    if y is not None:
        piece.y = y
    else:
        drop_to_bottom(board, piece)
    board.lock(piece)


class TestDropAndLock:
    def test_piece_lands_on_floor(self):
        b = Board()
        p = Tetromino(TetrominoType.O, x=3, y=0)
        drop_to_bottom(b, p)
        b.lock(p)
        # O piece 0° → rows 0,1 사용 → y=18 착지
        assert p.y == 18
        assert b.get(4, 18) == TetrominoType.O.value

    def test_piece_stacks_on_locked_piece(self):
        b = Board()
        p1 = Tetromino(TetrominoType.O, x=3, y=0)
        drop_to_bottom(b, p1)
        b.lock(p1)

        p2 = Tetromino(TetrominoType.O, x=3, y=0)
        drop_to_bottom(b, p2)
        b.lock(p2)
        # 두 번째 블록은 첫 번째 위에 쌓임
        assert p2.y == p1.y - 2


class TestLineClearIntegration:
    def _fill_row_except(self, board: Board, y: int, gap_x: int):
        for x in range(board.WIDTH):
            if x != gap_x:
                board._grid[y][x] = 1

    def test_single_line_clear_scores_correctly(self):
        b = Board()
        sm = ScoreManager()
        # 마지막 행 9칸 채우고 I 블록으로 마저 채움
        self._fill_row_except(b, 19, gap_x=0)
        p = Tetromino(TetrominoType.I, x=-3, y=18)
        # I 0° → y+1 행에 셀 위치
        p.y = 18
        b.lock(p)
        cleared = b.clear_lines()
        sm.add_clear(cleared)
        assert cleared == 1
        assert sm.score == 100

    def test_tetris_four_lines_clear(self):
        b = Board()
        sm = ScoreManager()
        for y in range(16, 20):
            for x in range(b.WIDTH):
                b._grid[y][x] = 1
        cleared = b.clear_lines()
        sm.add_clear(cleared)
        assert cleared == 4
        assert sm.score == 800

    def test_board_height_intact_after_multiple_clears(self):
        b = Board()
        for y in range(10, 20):
            for x in range(b.WIDTH):
                b._grid[y][x] = 1
        b.clear_lines()
        assert len(b._grid) == b.HEIGHT


class TestHardDropScoring:
    def test_hard_drop_score_equals_twice_distance(self):
        b = Board()
        sm = ScoreManager()
        p = Tetromino(TetrominoType.T, x=3, y=0)
        dist = b.ghost_y(p) - p.y
        p.y += dist
        sm.add_hard_drop(dist)
        b.lock(p)
        assert sm.score == dist * 2


class TestGameOverCondition:
    def test_spawn_blocked_causes_game_over_condition(self):
        b = Board()
        # I 블록 0° 셀은 행 1(y=1)에 위치하므로 행 0·1 모두 채워야 모든 블록 차단
        for x in range(b.WIDTH):
            b._grid[0][x] = 1
            b._grid[1][x] = 1
        new_piece = TetrominoFactory.random()
        assert not b.is_valid(new_piece)

    def test_normal_spawn_is_valid(self):
        b = Board()
        new_piece = TetrominoFactory.random()
        assert b.is_valid(new_piece)


class TestRotationAtWall:
    def test_rotate_at_right_wall_stays_if_invalid(self):
        b = Board()
        p = Tetromino(TetrominoType.I, x=8, y=5)
        original_rot = p.rotation
        p.rotate_cw()
        if not b.is_valid(p):
            p.rotate_ccw()
        # 회전 불가면 원래 상태 복귀
        assert p.rotation == original_rot or b.is_valid(p)

    def test_rotation_never_causes_out_of_bounds_lock(self):
        b = Board()
        for t in TetrominoType:
            p = Tetromino(t, x=3, y=10)
            for _ in range(4):
                p.rotate_cw()
                if b.is_valid(p):
                    for bx, by in p.get_cells():
                        assert 0 <= bx < b.WIDTH
                        assert by < b.HEIGHT
                else:
                    p.rotate_ccw()
