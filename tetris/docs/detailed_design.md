# 테트리스 게임 - 상세 설계서

## 1. 클래스 다이어그램

```
┌─────────────────────────────────┐
│         TetrominoType (Enum)    │
├─────────────────────────────────┤
│  I=1, O=2, T=3, S=4             │
│  Z=5, J=6, L=7                  │
└─────────────────────────────────┘

┌─────────────────────────────────┐      ┌──────────────────────────────┐
│           Tetromino             │      │      TetrominoFactory        │
├─────────────────────────────────┤      ├──────────────────────────────┤
│  + type: TetrominoType          │      │  (static methods only)       │
│  + x: int                       │◄─────│  + create(t:TetrominoType)   │
│  + y: int                       │      │  + random() → Tetromino      │
│  + rotation: int  (0~3)         │      └──────────────────────────────┘
│  + color: tuple[int,int,int]    │
├─────────────────────────────────┤
│  + get_cells() → list[tuple]    │
│  + rotate_cw() → None           │
│  + rotate_ccw() → None          │
│  + copy() → Tetromino           │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│             Board               │
├─────────────────────────────────┤
│  + WIDTH: int = 10              │
│  + HEIGHT: int = 20             │
│  - _grid: list[list[int]]       │
├─────────────────────────────────┤
│  + get(x,y) → int               │
│  + is_valid(piece, dx, dy) → bool│
│  + lock(piece) → None           │
│  + clear_lines() → int          │
│  + ghost_y(piece) → int         │
│  + is_game_over() → bool        │
│  + reset() → None               │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│          ScoreManager           │
├─────────────────────────────────┤
│  + score: int                   │
│  + level: int                   │
│  + lines: int                   │
│  - _SCORE_TABLE: dict           │
│  - _LINES_PER_LEVEL: int = 10   │
├─────────────────────────────────┤
│  + add_clear(n: int) → None     │
│  + add_soft_drop(n: int) → None │
│  + add_hard_drop(n: int) → None │
│  + fall_interval() → float      │
│  + reset() → None               │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│           Action (Enum)         │
├─────────────────────────────────┤
│  MOVE_LEFT, MOVE_RIGHT          │
│  MOVE_DOWN, ROTATE              │
│  HARD_DROP                      │
│  PAUSE, RESTART, QUIT           │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│          InputHandler           │
├─────────────────────────────────┤
│  - _REPEAT_DELAY: int = 150     │
│  - _REPEAT_INTERVAL: int = 50   │
│  - _held: dict[int, float]      │
├─────────────────────────────────┤
│  + poll(dt: float) → list[Action]│
└─────────────────────────────────┘

┌─────────────────────────────────┐
│            Renderer             │
├─────────────────────────────────┤
│  - _screen: pygame.Surface      │
│  - _font_lg: pygame.font.Font   │
│  - _font_sm: pygame.font.Font   │
│  - CELL = 30                    │
│  - OX = 50, OY = 50             │
├─────────────────────────────────┤
│  + draw_frame(ctx: RenderCtx)   │
│  - _draw_board(board)           │
│  - _draw_piece(piece, alpha)    │
│  - _draw_ghost(board, piece)    │
│  - _draw_panel(sm, next_piece)  │
│  - _draw_overlay(state, sm)     │
└─────────────────────────────────┘

┌─────────────────────────────────┐      ┌──────────────────────────────┐
│          GameState (Enum)       │      │         RenderCtx            │
├─────────────────────────────────┤      ├──────────────────────────────┤
│  PLAYING, PAUSED, GAME_OVER     │      │  board: Board                │
└─────────────────────────────────┘      │  piece: Tetromino            │
                                         │  next_piece: Tetromino       │
┌─────────────────────────────────┐      │  score: ScoreManager         │
│          GameManager            │      │  state: GameState            │
├─────────────────────────────────┤      └──────────────────────────────┘
│  - _board: Board                │
│  - _piece: Tetromino            │
│  - _next: Tetromino             │
│  - _score: ScoreManager         │
│  - _renderer: Renderer          │
│  - _input: InputHandler         │
│  - _state: GameState            │
│  - _fall_acc: float             │
│  - FPS: int = 60                │
├─────────────────────────────────┤
│  + run() → None                 │
│  - _handle(actions) → None      │
│  - _update(dt: float) → None    │
│  - _spawn() → None              │
│  - _lock_and_clear() → None     │
│  - _reset() → None              │
└─────────────────────────────────┘
```

---

## 2. 데이터 구조 정의

### 2.1 게임 보드 격자

```python
# Board._grid: 2차원 리스트
# 행(row) 0이 최상단, 행 19가 최하단
# 값: 0=빈칸, 1~7=TetrominoType 값(색상 ID)

_grid: list[list[int]] = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # row 0  (최상단)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # row 1
    ...
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # row 19 (최하단)
]
# 인덱스 접근: _grid[y][x]
```

### 2.2 테트로미노 회전 행렬

각 테트로미노는 4가지 회전 상태(0°, 90°, 180°, 270°)를 4×4 행렬로 저장합니다.
`1`은 블록, `0`은 빈칸입니다.

```python
SHAPES: dict[TetrominoType, list[list[list[int]]]] = {

    TetrominoType.I: [
        [[0,0,0,0],   # 0°
         [1,1,1,1],
         [0,0,0,0],
         [0,0,0,0]],
        [[0,0,1,0],   # 90°
         [0,0,1,0],
         [0,0,1,0],
         [0,0,1,0]],
        [[0,0,0,0],   # 180°
         [0,0,0,0],
         [1,1,1,1],
         [0,0,0,0]],
        [[0,1,0,0],   # 270°
         [0,1,0,0],
         [0,1,0,0],
         [0,1,0,0]],
    ],

    TetrominoType.O: [
        [[0,1,1,0],   # 0° (회전 없음 — 4개 상태 동일)
         [0,1,1,0],
         [0,0,0,0],
         [0,0,0,0]],
        ... # 나머지 3개 동일
    ],

    TetrominoType.T: [
        [[0,1,0,0],   # 0°
         [1,1,1,0],
         [0,0,0,0],
         [0,0,0,0]],
        [[0,1,0,0],   # 90°
         [0,1,1,0],
         [0,1,0,0],
         [0,0,0,0]],
        [[0,0,0,0],   # 180°
         [1,1,1,0],
         [0,1,0,0],
         [0,0,0,0]],
        [[0,1,0,0],   # 270°
         [1,1,0,0],
         [0,1,0,0],
         [0,0,0,0]],
    ],

    # S, Z, J, L 동일한 방식으로 정의
}
```

### 2.3 블록 색상 테이블

```python
COLORS: dict[TetrominoType, tuple[int, int, int]] = {
    TetrominoType.I: (0,   240, 240),   # 청록
    TetrominoType.O: (240, 240, 0  ),   # 노랑
    TetrominoType.T: (160, 0,   240),   # 보라
    TetrominoType.S: (0,   240, 0  ),   # 초록
    TetrominoType.Z: (240, 0,   0  ),   # 빨강
    TetrominoType.J: (0,   0,   240),   # 파랑
    TetrominoType.L: (240, 160, 0  ),   # 주황
}
GHOST_ALPHA = 80   # 고스트 피스 투명도 (0~255)
EMPTY_COLOR  = (30, 30, 30)   # 빈 칸 배경색
GRID_COLOR   = (50, 50, 50)   # 격자선 색
```

### 2.4 게임 상태 Enum

```python
from enum import Enum, auto

class GameState(Enum):
    PLAYING   = auto()
    PAUSED    = auto()
    GAME_OVER = auto()
```

---

## 3. 알고리즘 설계

### 3.1 블록 셀 좌표 추출 (`get_cells`)

```
입력: Tetromino (shape 4×4 행렬, x, y 위치)
출력: 보드 상의 절대 좌표 목록 [(bx, by), ...]

for row in 0..3:
    for col in 0..3:
        if shape[row][col] == 1:
            yield (piece.x + col, piece.y + row)
```

### 3.2 충돌 감지 (`is_valid`)

```
입력: piece, dx(이동량), dy(이동량)
출력: bool (이동 가능 여부)

임시 복사본 생성 (piece.copy())
임시 복사본 위치 += (dx, dy)
임시 복사본의 get_cells() 순회:
    if bx < 0 또는 bx >= WIDTH   → False (좌우 벽)
    if by >= HEIGHT               → False (하단 벽)
    if by >= 0 and _grid[by][bx] != 0 → False (다른 블록)
모두 통과 → True

※ by < 0 (보드 위) 은 충돌로 처리하지 않는다 (생성 직후 상태 허용)
```

### 3.3 줄 완성 판별 및 삭제 (`clear_lines`)

```
입력: _grid
출력: 삭제된 줄 수 (int)

완성된 줄 인덱스 수집:
    for y in 0..HEIGHT-1:
        if all(_grid[y][x] != 0 for x in 0..WIDTH-1):
            완성_목록.append(y)

완성된 줄 제거:
    for y in 완성_목록 (역순):
        _grid.pop(y)

상단에 빈 줄 삽입:
    for _ in range(len(완성_목록)):
        _grid.insert(0, [0] * WIDTH)

return len(완성_목록)
```

### 3.4 고스트 피스 위치 계산 (`ghost_y`)

```
입력: piece
출력: 고스트 피스의 y 좌표 (int)

ghost_y = piece.y
while is_valid(piece, dx=0, dy=ghost_y - piece.y + 1):
    ghost_y += 1

return ghost_y
```

### 3.4-1 회전 방식 결정: 단순 회전 취소 (SRS 미적용)

> **설계 결정 사항**: 초기 설계에서 SRS(Super Rotation System) 적용을 검토했으나, 구현 단계에서 **단순 회전 취소 방식**을 채택하였다.

**단순 회전 취소 방식 (구현 채택)**

```
rotate_cw() 호출
if not is_valid(piece):
    rotate_ccw()   # 원래 상태로 복귀
```

회전 후 충돌이 발생하면 즉시 원래 회전 상태로 되돌린다. 벽 킥(wall kick)이나 위치 보정을 시도하지 않는다.

**SRS 미채택 이유**

| 항목 | 내용 |
|------|------|
| 구현 복잡도 | SRS는 블록/회전 상태별 5개의 킥 오프셋 테이블이 필요하며 코드량이 크게 증가 |
| 1차 목표 범위 | 클래식 테트리스 규칙 구현이 목표이며 경쟁적 플레이 지원이 아님 |
| 향후 확장 가능 | `rotate_cw()` 호출부(`game.py _handle`)를 교체하는 것만으로 SRS로 업그레이드 가능 |

---

### 3.5 하드 드롭 (`hard_drop`)

```
낙하 거리 = ghost_y(piece) - piece.y
piece.y   = ghost_y(piece)
score.add_hard_drop(낙하 거리)
_lock_and_clear()
```

### 3.6 자동 낙하 (`_update`)

```
입력: dt (이전 프레임과의 경과 시간, 초 단위)

_fall_acc += dt
if _fall_acc >= score.fall_interval():
    _fall_acc -= score.fall_interval()
    if is_valid(piece, dx=0, dy=1):
        piece.y += 1
    else:
        _lock_and_clear()   # 바닥 도달 → 고정
```

### 3.7 레벨별 낙하 간격 (`fall_interval`)

```
NES 테트리스 공식 기반:
frames_per_cell = (0.8 - (level - 1) * 0.007) ^ (level - 1)

level  1 → 1.000s
level  5 → 0.355s
level 10 → 0.083s
level 15 → 0.020s  (최소값)
```

### 3.8 키 반복 처리 (`InputHandler.poll`)

```
입력: dt (경과 시간 ms)
출력: list[Action]

이벤트 큐에서 KEYDOWN / KEYUP 처리:
    KEYDOWN → _held[key] = 0.0       # 누른 시각 초기화
    KEYUP   → _held.pop(key)

결과 목록 생성:
    for key, held_time in _held.items():
        if held_time == 0.0:              # 처음 눌린 프레임
            결과.append(key_to_action(key))
            _held[key] = REPEAT_DELAY
        else:
            _held[key] -= dt
            if _held[key] <= 0:
                결과.append(key_to_action(key))
                _held[key] += REPEAT_INTERVAL

return 결과
```

---

## 4. 화면 좌표 변환

보드 격자 좌표 `(bx, by)` → 픽셀 좌표 `(px, py)`

```python
CELL = 30   # px
OX   = 50   # 보드 좌측 상단 X 오프셋
OY   = 50   # 보드 좌측 상단 Y 오프셋

px = OX + bx * CELL
py = OY + by * CELL
```

---

## 5. 파일별 상수 정의 위치

| 상수 | 정의 위치 | 값 |
| ---- | --------- | -- |
| `BOARD_WIDTH`, `BOARD_HEIGHT` | `board.py` | 10, 20 |
| `SHAPES`, `COLORS` | `tetromino.py` | 각 블록 행렬/색상 |
| `SCORE_TABLE`, `LINES_PER_LEVEL` | `score.py` | {1:100, 2:300, ...}, 10 |
| `CELL`, `OX`, `OY`, `FPS` | `renderer.py` | 30, 50, 50, 60 |
| `REPEAT_DELAY`, `REPEAT_INTERVAL` | `input_handler.py` | 150, 50 |

---

## 6. 예외 및 엣지 케이스 처리

| 상황 | 처리 방법 |
| ---- | --------- |
| 블록 생성 위치에 이미 블록 존재 | `is_game_over()` 반환 → GAME_OVER 전환 |
| 회전 시 벽/블록과 겹침 | `is_valid` 실패 시 회전 취소 (원래 상태 유지) — SRS 벽 킥 미적용 |
| 보드 상단 위(y < 0) 에서 회전 | `is_valid`에서 y < 0 허용으로 생성 직후 회전 가능 |
| 4줄 동시 삭제 (테트리스) | `clear_lines`가 리스트 순회로 자연스럽게 처리 |
| 레벨 15 초과 | `fall_interval()`에서 최솟값 0.020s 클램프 |

---

## 진행 상황 업데이트

> **DESIGN_PROCESS.md** 진행 표 업데이트 필요
> - [x] 3단계: 상세 설계 — **완료**
