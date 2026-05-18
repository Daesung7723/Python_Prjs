import pytest
from src.score import ScoreManager


@pytest.fixture
def sm():
    return ScoreManager()


class TestInitialState:
    def test_initial_score_zero(self, sm):
        assert sm.score == 0

    def test_initial_level_one(self, sm):
        assert sm.level == 1

    def test_initial_lines_zero(self, sm):
        assert sm.lines == 0


class TestLineClear:
    @pytest.mark.parametrize("lines,expected", [
        (1, 100),
        (2, 300),
        (3, 500),
        (4, 800),
    ])
    def test_score_at_level1(self, sm, lines, expected):
        sm.add_clear(lines)
        assert sm.score == expected

    def test_score_multiplied_by_level(self, sm):
        sm.level = 3
        sm.add_clear(1)
        assert sm.score == 300  # 100 * 3

    def test_tetris_at_level2(self, sm):
        sm.level = 2
        sm.add_clear(4)
        assert sm.score == 1600  # 800 * 2

    def test_lines_accumulate(self, sm):
        sm.add_clear(2)
        sm.add_clear(2)
        assert sm.lines == 4

    def test_zero_clear_no_change(self, sm):
        sm.add_clear(0)
        assert sm.score == 0
        assert sm.lines == 0


class TestLevelProgression:
    def test_level_up_after_10_lines(self, sm):
        sm.add_clear(1)  # 1줄
        assert sm.level == 1
        for _ in range(9):
            sm.add_clear(1)  # 누적 10줄
        assert sm.level == 2

    def test_level_up_after_tetris(self, sm):
        sm.add_clear(4)   # 4줄
        sm.add_clear(4)   # 8줄
        sm.add_clear(2)   # 10줄 → 레벨 2
        assert sm.level == 2

    def test_max_level_is_15(self, sm):
        for _ in range(20):
            sm.add_clear(4)  # 80줄 → 레벨 9
        sm.lines = 200       # 강제로 넘김
        sm.add_clear(1)
        assert sm.level == 15

    def test_score_uses_updated_level(self, sm):
        # 10줄 소거로 레벨 2가 된 후 추가 소거
        for _ in range(10):
            sm.add_clear(1)
        score_before = sm.score
        sm.add_clear(1)
        assert sm.score - score_before == 100 * 2  # 레벨 2


class TestDropScore:
    def test_soft_drop_adds_one_per_cell(self, sm):
        sm.add_soft_drop(5)
        assert sm.score == 5

    def test_hard_drop_adds_two_per_cell(self, sm):
        sm.add_hard_drop(10)
        assert sm.score == 20

    def test_soft_drop_default_one(self, sm):
        sm.add_soft_drop()
        assert sm.score == 1


class TestFallInterval:
    def test_level1_is_one_second(self, sm):
        assert sm.fall_interval() == pytest.approx(1.0, rel=1e-3)

    def test_higher_level_is_faster(self, sm):
        sm.level = 1
        t1 = sm.fall_interval()
        sm.level = 5
        t5 = sm.fall_interval()
        assert t5 < t1

    def test_level15_clamped_to_minimum(self, sm):
        sm.level = 15
        assert sm.fall_interval() == pytest.approx(0.020, abs=1e-4)

    def test_level_above_15_same_as_15(self, sm):
        sm.level = 15
        t15 = sm.fall_interval()
        sm.level = 20
        assert sm.fall_interval() == pytest.approx(t15, rel=1e-6)


class TestReset:
    def test_reset_restores_initial_state(self, sm):
        sm.add_clear(4)
        sm.add_hard_drop(10)
        sm.reset()
        assert sm.score == 0
        assert sm.level == 1
        assert sm.lines == 0
