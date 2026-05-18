from __future__ import annotations
import pygame
from src.board import Board
from src.tetromino import TetrominoFactory
from src.score import ScoreManager
from src.renderer import Renderer, RenderCtx
from src.input_handler import InputHandler, Action
from src.game_state import GameState


class GameManager:
    FPS = 60

    def __init__(self) -> None:
        pygame.init()
        self._board    = Board()
        self._score    = ScoreManager()
        self._renderer = Renderer()
        self._input    = InputHandler()
        self._next     = TetrominoFactory.random()
        self._piece    = TetrominoFactory.random()
        self._state    = GameState.PLAYING
        self._fall_acc = 0.0
        self._clock    = pygame.time.Clock()

    def run(self) -> None:
        while True:
            dt = self._clock.tick(self.FPS)  # ms

            actions = self._input.poll(dt)

            if Action.QUIT in actions:
                break

            match self._state:
                case GameState.PLAYING:
                    self._handle(actions, dt)
                case GameState.PAUSED:
                    if Action.RESTART in actions:
                        self._reset()
                    elif Action.PAUSE in actions:
                        self._state = GameState.PLAYING
                case GameState.GAME_OVER:
                    if Action.RESTART in actions:
                        self._reset()

            self._renderer.draw_frame(RenderCtx(
                board=self._board,
                piece=self._piece,
                next_piece=self._next,
                score=self._score,
                state=self._state,
            ))

        pygame.quit()

    # ── game logic ───────────────────────────────────────────────────────

    def _handle(self, actions: list[Action], dt: float) -> None:
        for action in actions:
            match action:
                case Action.MOVE_LEFT:
                    if self._board.is_valid(self._piece, dx=-1):
                        self._piece.x -= 1
                case Action.MOVE_RIGHT:
                    if self._board.is_valid(self._piece, dx=1):
                        self._piece.x += 1
                case Action.MOVE_DOWN:
                    if self._board.is_valid(self._piece, dy=1):
                        self._piece.y += 1
                        self._score.add_soft_drop()
                    else:
                        self._lock_and_clear()
                        return
                case Action.ROTATE:
                    self._piece.rotate_cw()
                    if not self._board.is_valid(self._piece):
                        self._piece.rotate_ccw()
                case Action.HARD_DROP:
                    drop = self._board.ghost_y(self._piece) - self._piece.y
                    self._piece.y += drop
                    self._score.add_hard_drop(drop)
                    self._lock_and_clear()
                    return
                case Action.PAUSE:
                    self._state = GameState.PAUSED

        # 자동 낙하
        self._fall_acc += dt
        interval_ms = self._score.fall_interval() * 1000
        while self._fall_acc >= interval_ms:
            self._fall_acc -= interval_ms
            if self._board.is_valid(self._piece, dy=1):
                self._piece.y += 1
            else:
                self._lock_and_clear()
                return

    def _lock_and_clear(self) -> None:
        self._board.lock(self._piece)
        cleared = self._board.clear_lines()
        if cleared:
            self._score.add_clear(cleared)
        self._fall_acc = 0.0
        self._spawn()

    def _spawn(self) -> None:
        self._piece      = self._next
        self._next       = TetrominoFactory.random()
        if not self._board.is_valid(self._piece):
            self._state = GameState.GAME_OVER

    def _reset(self) -> None:
        self._board.reset()
        self._score.reset()
        self._next     = TetrominoFactory.random()
        self._piece    = TetrominoFactory.random()
        self._fall_acc = 0.0
        self._state    = GameState.PLAYING
