from __future__ import annotations
from enum import Enum, auto
import pygame


class Action(Enum):
    MOVE_LEFT  = auto()
    MOVE_RIGHT = auto()
    MOVE_DOWN  = auto()
    ROTATE     = auto()
    HARD_DROP  = auto()
    PAUSE      = auto()
    RESTART    = auto()
    QUIT       = auto()


_KEY_MAP: dict[int, Action] = {
    pygame.K_LEFT:   Action.MOVE_LEFT,
    pygame.K_RIGHT:  Action.MOVE_RIGHT,
    pygame.K_DOWN:   Action.MOVE_DOWN,
    pygame.K_UP:     Action.ROTATE,
    pygame.K_SPACE:  Action.HARD_DROP,
    pygame.K_p:      Action.PAUSE,
    pygame.K_r:      Action.RESTART,
    pygame.K_q:      Action.QUIT,
    pygame.K_ESCAPE: Action.QUIT,
}

_REPEATABLE     = {Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.MOVE_DOWN}
_REPEAT_DELAY   = 150  # ms before key repeat begins
_REPEAT_INTERVAL = 50  # ms between repeated actions


class InputHandler:
    def __init__(self) -> None:
        # key code → ms remaining until next repeat fire
        self._held: dict[int, float] = {}

    def poll(self, dt: float) -> list[Action]:
        actions: list[Action] = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                actions.append(Action.QUIT)
            elif event.type == pygame.KEYDOWN:
                action = _KEY_MAP.get(event.key)
                if action:
                    actions.append(action)
                    if action in _REPEATABLE:
                        self._held[event.key] = float(_REPEAT_DELAY)
            elif event.type == pygame.KEYUP:
                self._held.pop(event.key, None)

        for key in list(self._held):
            self._held[key] -= dt
            if self._held[key] <= 0:
                action = _KEY_MAP.get(key)
                if action and action in _REPEATABLE:
                    actions.append(action)
                self._held[key] += _REPEAT_INTERVAL

        return actions
