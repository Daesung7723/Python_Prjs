# Python Tetris

키보드 방향키와 스페이스바로 조작하는 클래식 테트리스 게임입니다.

---

## 요구 사항

- Python 3.10 이상
- pygame 2.0 이상

---

## 설치 및 실행

```bash
# 1. 저장소 클론 또는 폴더 이동
cd tetris

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 게임 실행
python main.py
```

---

## 키보드 조작

| 키 | 동작 |
| -- | ---- |
| `←` / `→` | 블록 좌우 이동 |
| `↓` | 블록 빠르게 낙하 (소프트 드롭, +1점/칸) |
| `↑` | 블록 시계방향 회전 |
| `Space` | 즉시 바닥까지 낙하 (하드 드롭, +2점/칸) |
| `P` | 일시정지 / 재개 |
| `R` | 게임 재시작 |
| `Q` / `ESC` | 게임 종료 |

---

## 점수 시스템

| 동작 | 점수 |
| ---- | ---- |
| 1줄 삭제 (Single) | 100 × 레벨 |
| 2줄 삭제 (Double) | 300 × 레벨 |
| 3줄 삭제 (Triple) | 500 × 레벨 |
| 4줄 삭제 (Tetris) | 800 × 레벨 |
| 소프트 드롭 | 1점 × 낙하 칸 수 |
| 하드 드롭 | 2점 × 낙하 칸 수 |

10줄 삭제마다 레벨이 오르고, 레벨이 높아질수록 블록 낙하 속도가 빨라집니다. 최대 레벨은 15입니다.

---

## 프로젝트 구조

```text
tetris/
├── main.py                  # 진입점
├── requirements.txt
├── README.md
├── src/
│   ├── game_state.py        # GameState Enum
│   ├── tetromino.py         # 7종 블록 정의 · 회전
│   ├── board.py             # 10×20 보드 · 충돌 · 줄 삭제
│   ├── score.py             # 점수 · 레벨 관리
│   ├── input_handler.py     # 키보드 입력 · 키 반복 처리
│   ├── renderer.py          # pygame 렌더링 · 고스트 피스
│   └── game.py              # 게임 루프 · 상태 머신
├── tests/
│   ├── test_tetromino.py
│   ├── test_board.py
│   ├── test_score.py
│   └── test_integration.py
└── docs/
    ├── DESIGN_PROCESS.md
    ├── requirements.md
    ├── system_design.md
    └── detailed_design.md
```

---

## 테스트 실행

```bash
pip install pytest
python -m pytest tests/ -v
```

총 82개 테스트, 전체 통과 확인.

---

## 테트로미노 종류

| 블록 | 색상 |
| ---- | ---- |
| I | 청록 |
| O | 노랑 |
| T | 보라 |
| S | 초록 |
| Z | 빨강 |
| J | 파랑 |
| L | 주황 |
