import pytest
from src.tetromino import Tetromino, TetrominoType, TetrominoFactory, SHAPES, COLORS


class TestTetrominoShape:
    def test_all_types_have_four_rotations(self):
        for t in TetrominoType:
            assert len(SHAPES[t]) == 4, f"{t} 회전 상태 4개 필요"

    def test_each_rotation_is_4x4(self):
        for t in TetrominoType:
            for rot in SHAPES[t]:
                assert len(rot) == 4
                for row in rot:
                    assert len(row) == 4

    def test_all_types_have_color(self):
        for t in TetrominoType:
            assert t in COLORS
            r, g, b = COLORS[t]
            assert 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255

    def test_i_piece_horizontal_has_four_cells_in_row(self):
        shape = SHAPES[TetrominoType.I][0]
        flat = [cell for row in shape for cell in row]
        assert flat.count(1) == 4
        # 4칸이 한 행에 연속
        filled_rows = [i for i, row in enumerate(shape) if 1 in row]
        assert len(filled_rows) == 1

    def test_o_piece_all_rotations_identical(self):
        rotations = SHAPES[TetrominoType.O]
        for r in rotations[1:]:
            assert r == rotations[0]

    @pytest.mark.parametrize("t", list(TetrominoType))
    def test_each_piece_has_exactly_four_filled_cells(self, t):
        shape = SHAPES[t][0]
        count = sum(cell for row in shape for cell in row)
        assert count == 4, f"{t} 블록은 4칸이어야 함"


class TestTetrominoInstance:
    def test_default_spawn_position(self):
        p = Tetromino(TetrominoType.T)
        assert p.x == 3
        assert p.y == 0
        assert p.rotation == 0

    def test_get_cells_returns_four_coords(self):
        p = Tetromino(TetrominoType.T)
        cells = p.get_cells()
        assert len(cells) == 4

    def test_get_cells_offset_by_position(self):
        p = Tetromino(TetrominoType.O, x=2, y=5)
        cells = p.get_cells()
        xs = [c[0] for c in cells]
        ys = [c[1] for c in cells]
        assert min(xs) >= 2
        assert min(ys) >= 5

    def test_rotate_cw_increments_rotation(self):
        p = Tetromino(TetrominoType.T)
        p.rotate_cw()
        assert p.rotation == 1

    def test_rotate_cw_wraps_at_four(self):
        p = Tetromino(TetrominoType.T)
        for _ in range(4):
            p.rotate_cw()
        assert p.rotation == 0

    def test_rotate_ccw_decrements_rotation(self):
        p = Tetromino(TetrominoType.T)
        p.rotate_ccw()
        assert p.rotation == 3

    def test_rotate_cw_then_ccw_restores_state(self):
        p = Tetromino(TetrominoType.S)
        original = p.shape
        p.rotate_cw()
        p.rotate_ccw()
        assert p.shape == original

    def test_copy_is_independent(self):
        p = Tetromino(TetrominoType.L, x=2, y=3)
        p.rotation = 2
        c = p.copy()
        assert c.x == 2 and c.y == 3 and c.rotation == 2
        c.x = 99
        c.rotate_cw()
        assert p.x == 2
        assert p.rotation == 2


class TestTetrominoFactory:
    def test_create_returns_correct_type(self):
        for t in TetrominoType:
            p = TetrominoFactory.create(t)
            assert p.type == t

    def test_random_returns_tetromino(self):
        p = TetrominoFactory.random()
        assert isinstance(p, Tetromino)
        assert p.type in TetrominoType
