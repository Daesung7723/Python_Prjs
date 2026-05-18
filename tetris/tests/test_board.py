import pytest
from src.board import Board
from src.tetromino import Tetromino, TetrominoType, TetrominoFactory


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def t_piece():
    return Tetromino(TetrominoType.T, x=3, y=5)


class TestBoardInit:
    def test_dimensions(self, board):
        assert board.WIDTH == 10
        assert board.HEIGHT == 20

    def test_all_cells_empty(self, board):
        for y in range(board.HEIGHT):
            for x in range(board.WIDTH):
                assert board.get(x, y) == 0

    def test_out_of_bounds_returns_zero(self, board):
        assert board.get(-1, 0) == 0
        assert board.get(10, 0) == 0
        assert board.get(0, 20) == 0


class TestIsValid:
    def test_fresh_piece_at_spawn_is_valid(self, board):
        p = TetrominoFactory.create(TetrominoType.T)
        assert board.is_valid(p)

    def test_move_into_left_wall_invalid(self, board):
        p = Tetromino(TetrominoType.I, x=0, y=5)
        assert not board.is_valid(p, dx=-1)

    def test_move_into_right_wall_invalid(self, board):
        p = Tetromino(TetrominoType.I, x=7, y=5)
        assert not board.is_valid(p, dx=3)

    def test_move_below_floor_invalid(self, board):
        p = Tetromino(TetrominoType.O, x=3, y=18)
        assert not board.is_valid(p, dy=3)

    def test_move_into_locked_block_invalid(self, board):
        board._grid[10][4] = 1
        p = Tetromino(TetrominoType.O, x=3, y=8)
        # O piece at x=3,y=8 occupies (4,8),(5,8),(4,9),(5,9)
        # 아래로 2칸 이동 시 (4,10),(5,10) 충돌
        assert not board.is_valid(p, dy=2)

    def test_piece_above_board_allowed(self, board):
        # 생성 직후 y<0 영역은 허용
        p = Tetromino(TetrominoType.I, x=3, y=-1)
        assert board.is_valid(p)

    def test_valid_horizontal_move(self, board, t_piece):
        assert board.is_valid(t_piece, dx=1)
        assert board.is_valid(t_piece, dx=-1)

    def test_valid_downward_move(self, board, t_piece):
        assert board.is_valid(t_piece, dy=1)


class TestLock:
    def test_lock_writes_type_value_to_grid(self, board):
        p = Tetromino(TetrominoType.T, x=3, y=10)
        board.lock(p)
        for bx, by in p.get_cells():
            assert board.get(bx, by) == TetrominoType.T.value

    def test_lock_ignores_cells_with_negative_y(self, board):
        # I 0° row1=[1,1,1,1] → y=-2+1=-1 (음수, 무시) → 보드에 아무것도 기록 안 됨
        p = Tetromino(TetrominoType.I, x=3, y=-2)
        board.lock(p)
        assert all(board.get(x, 0) == 0 for x in range(board.WIDTH))


class TestClearLines:
    def _fill_row(self, board, y):
        for x in range(board.WIDTH):
            board._grid[y][x] = 1

    def test_no_full_lines_returns_zero(self, board):
        assert board.clear_lines() == 0

    def test_one_full_line_returns_one(self, board):
        self._fill_row(board, 19)
        assert board.clear_lines() == 1

    def test_cleared_line_replaced_by_empty_top(self, board):
        self._fill_row(board, 19)
        board.clear_lines()
        assert all(board.get(x, 0) == 0 for x in range(board.WIDTH))

    def test_four_lines_cleared_at_once(self, board):
        for y in range(16, 20):
            self._fill_row(board, y)
        assert board.clear_lines() == 4

    def test_grid_height_unchanged_after_clear(self, board):
        for y in range(17, 20):
            self._fill_row(board, y)
        board.clear_lines()
        assert len(board._grid) == board.HEIGHT

    def test_rows_above_fall_down(self, board):
        # 19행 가득 채우고, 18행 중간에 마커 배치
        self._fill_row(board, 19)
        board._grid[18][0] = 2
        board.clear_lines()
        # 19행 삭제 → 18행이 19행으로 내려와야 함
        assert board.get(0, 19) == 2

    def test_partial_line_not_cleared(self, board):
        self._fill_row(board, 19)
        board._grid[19][5] = 0  # 한 칸 비움
        assert board.clear_lines() == 0


class TestGhostY:
    def test_ghost_lands_on_floor(self, board):
        p = Tetromino(TetrominoType.O, x=3, y=0)
        gy = board.ghost_y(p)
        # O piece 0° 행 0~1 사용 → 최대 y = HEIGHT-2 = 18
        assert gy == board.HEIGHT - 2

    def test_ghost_lands_on_locked_block(self, board):
        for x in range(board.WIDTH):
            board._grid[15][x] = 1
        p = Tetromino(TetrominoType.O, x=3, y=0)
        gy = board.ghost_y(p)
        assert gy == 13  # O piece는 2행 → 15행 위 13행에 착지

    def test_ghost_equals_piece_y_when_already_grounded(self, board):
        p = Tetromino(TetrominoType.O, x=3, y=18)
        gy = board.ghost_y(p)
        assert gy == p.y


class TestGameOver:
    def test_empty_board_not_game_over(self, board):
        assert not board.is_game_over()

    def test_block_in_top_row_is_game_over(self, board):
        board._grid[0][5] = 1
        assert board.is_game_over()

    def test_block_in_second_row_not_game_over(self, board):
        board._grid[1][5] = 1
        assert not board.is_game_over()


class TestReset:
    def test_reset_clears_grid(self, board):
        for x in range(board.WIDTH):
            board._grid[19][x] = 1
        board.reset()
        assert all(board.get(x, 19) == 0 for x in range(board.WIDTH))
