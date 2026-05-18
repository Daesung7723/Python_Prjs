# 테트리스 게임 - 시스템 설계서

## 1. 아키텍처 패턴: MVC (Model-View-Controller)

```
┌─────────────────────────────────────────────────────────────┐
│                        Game Loop (game.py)                  │
│                   매 프레임마다 순환 실행                      │
└───────────┬───────────────────┬───────────────────┬─────────┘
            │                   │                   │
            ▼                   ▼                   ▼
┌───────────────────┐ ┌─────────────────┐ ┌────────────────────┐
│   MODEL           │ │   VIEW          │ │   CONTROLLER       │
│                   │ │                 │ │                    │
│  board.py         │ │  renderer.py    │ │  input_handler.py  │
│  tetromino.py     │ │                 │ │                    │
│  score.py         │ │                 │ │                    │
└───────────────────┘ └─────────────────┘ └────────────────────┘
        │                     │                     │
        │◄────────────────────┤                     │
        │   상태 읽기          │                     │
        │                     │                     │
        │◄────────────────────────────────────────── │
                    사용자 입력 → 상태 변경
```

### 역할 분리 원칙

| 계층 | 파일 | 책임 |
|------|------|------|
| Model | `board.py` | 보드 격자 상태, 충돌 감지, 줄 삭제 |
| Model | `tetromino.py` | 블록 형태 정의, 회전 행렬, 위치 |
| Model | `score.py` | 점수 계산, 레벨 관리, 줄 수 집계 |
| Model | `game_state.py` | 게임 상태 Enum (PLAYING / PAUSED / GAME_OVER) |
| View | `renderer.py` | pygame 화면 렌더링, UI 요소 출력 |
| Controller | `input_handler.py` | 키보드 이벤트 수신 및 명령 변환 |
| Entry Point | `game.py` | 게임 루프, 상태 머신, 모듈 통합 |

---

## 2. 모듈 구조 및 의존 관계

```
main.py
  └── game.py (GameManager)
        ├── board.py (Board)          ← 게임 핵심 로직
        │     └── tetromino.py (Tetromino, TetrominoFactory)
        ├── score.py (ScoreManager)   ← 점수/레벨
        ├── renderer.py (Renderer)    ← 화면 출력
        ├── input_handler.py (InputHandler)  ← 키 입력
        └── game_state.py (GameState) ← 상태 Enum (설계 대비 별도 파일로 분리)
```

**의존 방향 규칙**
- `game.py`만 모든 모듈을 참조한다
- Model 모듈끼리 순환 참조를 허용하지 않는다
- `renderer.py`는 Model의 데이터를 읽기 전용으로 참조한다
- `input_handler.py`는 다른 모듈을 참조하지 않는다
- `game_state.py`는 의존성이 없는 독립 모듈이며 `game.py`와 `renderer.py`가 참조한다

---

## 3. 모듈별 책임 상세

### 3.1 `tetromino.py`

**역할**: 테트로미노의 형태 데이터와 회전 상태 관리

```
TetrominoType (Enum)
  I, O, T, S, Z, J, L

Tetromino
  - type: TetrominoType
  - shape: list[list[int]]   # 현재 회전 상태의 4×4 행렬
  - color: tuple             # RGB 색상
  - x, y: int                # 보드 상의 현재 위치
  + rotate() → None          # 시계방향 90도 회전
  + get_cells() → list       # 현재 블록이 차지하는 (x, y) 좌표 목록

TetrominoFactory
  + create(type) → Tetromino
  + random() → Tetromino
```

### 3.2 `board.py`

**역할**: 10×20 격자 상태 관리, 충돌 감지, 줄 삭제

```
Board
  - grid: list[list[int]]    # 10×20, 0=빈칸 / 1~7=색상ID
  - WIDTH = 10
  - HEIGHT = 20
  + is_valid_position(tetromino, dx, dy) → bool   # 이동 가능 여부
  + lock_tetromino(tetromino) → None              # 블록 고정
  + clear_lines() → int                           # 완성 줄 삭제 후 삭제 줄 수 반환
  + get_ghost_position(tetromino) → int           # 고스트 피스 y좌표
  + is_game_over() → bool
  + reset() → None
```

### 3.3 `score.py`

**역할**: 점수 계산 및 레벨 관리

```
ScoreManager
  - score: int
  - level: int
  - lines_cleared: int
  - LINES_PER_LEVEL = 10
  - LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}
  + add_line_clear(lines: int) → None   # 줄 삭제 점수 추가
  + add_soft_drop(cells: int) → None    # 소프트 드롭 점수
  + add_hard_drop(cells: int) → None    # 하드 드롭 점수
  + reset() → None
```

### 3.4 `renderer.py`

**역할**: pygame 기반 화면 렌더링

```
Renderer
  - screen: pygame.Surface
  - CELL_SIZE = 30           # 한 칸의 픽셀 크기
  - BOARD_OFFSET_X = 50      # 보드 좌측 여백
  - BOARD_OFFSET_Y = 50      # 보드 상단 여백
  + draw(board, tetromino, ghost, score_manager, next_piece) → None
  + draw_board(board) → None
  + draw_tetromino(tetromino) → None
  + draw_ghost(ghost_y, tetromino) → None
  + draw_ui(score_manager, next_piece) → None
  + draw_game_over(score_manager) → None
  + draw_pause() → None
```

### 3.5 `input_handler.py`

**역할**: pygame 키 이벤트를 게임 명령으로 변환

```
Action (Enum)
  MOVE_LEFT, MOVE_RIGHT, MOVE_DOWN, ROTATE
  HARD_DROP, PAUSE, RESTART, QUIT

InputHandler
  - KEY_REPEAT_DELAY = 150   # ms, 키 반복 시작 전 대기
  - KEY_REPEAT_INTERVAL = 50 # ms, 키 반복 간격
  + get_actions() → list[Action]   # 이번 프레임의 입력 목록 반환
```

### 3.6 `game_state.py`

**역할**: 게임 상태 Enum 정의 (설계 단계에서는 `game.py` 내부에 두기로 했으나, 구현 시 순환 참조 방지를 위해 별도 파일로 분리)

```
GameState (Enum)
  PLAYING, PAUSED, GAME_OVER
```

### 3.7 `game.py`

**역할**: 게임 루프 및 상태 머신

```
GameManager
  - state: GameState
  - board: Board
  - current_piece: Tetromino
  - next_piece: Tetromino
  - score_manager: ScoreManager
  - renderer: Renderer
  - input_handler: InputHandler
  - fall_timer: float          # 자동 낙하 타이머
  + run() → None               # 메인 루프 진입점
  - _handle_actions(actions) → None
  - _update() → None           # 자동 낙하, 상태 갱신
  - _spawn_next_piece() → None
  - _lock_and_clear() → None   # 블록 고정 + 줄 삭제 + 점수
```

---

## 4. 게임 상태 머신

```
              ┌─────────────────────────────────────┐
              │                                     │
    시작       ▼           P 키                     │
  ───────► PLAYING ─────────────────► PAUSED        │
              │           P 키 (재개)◄──             │
              │                                     │
              │ 블록이 상단 초과                      │
              ▼                                     │
           GAME_OVER                                │
              │                                     │
              │ R 키 (재시작)                        │
              └─────────────────────────────────────┘
```

---

## 5. 게임 루프 흐름

```
run()
  ├── pygame.init()
  ├── while True:
  │     ├── dt = clock.tick(FPS)          # 프레임 시간 측정
  │     ├── actions = input_handler.get_actions()
  │     │
  │     ├── [state == PLAYING]
  │     │     ├── _handle_actions(actions)  # 키 입력 처리
  │     │     └── _update(dt)               # 자동 낙하
  │     │
  │     ├── [state == PAUSED]
  │     │     └── P 키 감지 시 PLAYING 복귀
  │     │
  │     ├── [state == GAME_OVER]
  │     │     └── R 키 감지 시 재시작
  │     │
  │     └── renderer.draw(...)              # 매 프레임 렌더링
  │
  └── pygame.quit()
```

---

## 6. 화면 레이아웃

```
┌──────────────────────────────────────────────┐
│                                              │
│   ┌────────────────────┐   ┌──────────────┐  │
│   │                    │   │  NEXT PIECE  │  │
│   │                    │   │  ┌────────┐  │  │
│   │   GAME BOARD       │   │  │        │  │  │
│   │   (10 × 20)        │   │  └────────┘  │  │
│   │                    │   │              │  │
│   │                    │   │  SCORE       │  │
│   │                    │   │  000000      │  │
│   │                    │   │              │  │
│   │                    │   │  LEVEL       │  │
│   │                    │   │  01          │  │
│   │                    │   │              │  │
│   │                    │   │  LINES       │  │
│   │                    │   │  000         │  │
│   └────────────────────┘   └──────────────┘  │
│                                              │
└──────────────────────────────────────────────┘

전체 창 크기: 500 × 700 px
보드 영역:   300 × 600 px  (30px × 10칸 × 20칸)
사이드 패널: 150 × 600 px
```

---

## 7. 기술 스택 결정

| 항목 | 선택 | 이유 |
|------|------|------|
| 렌더링 | `pygame` | 키 입력 처리와 그래픽을 동시에 제공, Python 게임 개발 표준 |
| 언어 | Python 3.10+ | match 문 활용 가능, 타입 힌트 지원 |
| 테스트 | `pytest` | 단위 테스트 표준 프레임워크 |
| 패키지 관리 | `pip` + `requirements.txt` | 간단한 의존성 |

---

## 진행 상황 업데이트

> **DESIGN_PROCESS.md** 진행 표 업데이트 필요
> - [x] 2단계: 시스템 설계 — **완료**
