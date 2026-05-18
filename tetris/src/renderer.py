from __future__ import annotations
from dataclasses import dataclass
import pygame
from src.board import Board
from src.tetromino import Tetromino, COLORS, TetrominoType
from src.score import ScoreManager
from src.game_state import GameState

CELL    = 30
OX      = 50
OY      = 30
PANEL_X = OX + Board.WIDTH * CELL + 20
WIN_W   = PANEL_X + 150
WIN_H   = OY + Board.HEIGHT * CELL + 50

_BG       = (15,  15,  20)
_EMPTY    = (30,  30,  30)
_GRID     = (50,  50,  50)
_PANEL_BG = (25,  25,  35)
_WHITE    = (220, 220, 220)
_LABEL    = (140, 140, 160)
_YELLOW   = (240, 240, 0)
_GHOST_A  = 60


@dataclass
class RenderCtx:
    board:      Board
    piece:      Tetromino
    next_piece: Tetromino
    score:      ScoreManager
    state:      GameState


class Renderer:
    def __init__(self) -> None:
        self._screen   = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Tetris")
        self._font_lg  = pygame.font.SysFont("consolas", 26, bold=True)
        self._font_sm  = pygame.font.SysFont("consolas", 17)

    # ── public ──────────────────────────────────────────────────────────

    def draw_frame(self, ctx: RenderCtx) -> None:
        self._screen.fill(_BG)
        self._draw_board(ctx.board)
        if ctx.state == GameState.PLAYING:
            self._draw_ghost(ctx.board, ctx.piece)
            self._draw_piece(ctx.piece, 255)
        self._draw_panel(ctx.score, ctx.next_piece)
        if ctx.state == GameState.PAUSED:
            self._draw_overlay("PAUSED", "P: resume   R: restart")
        elif ctx.state == GameState.GAME_OVER:
            self._draw_game_over(ctx.score)
        pygame.display.flip()

    # ── private ─────────────────────────────────────────────────────────

    def _draw_board(self, board: Board) -> None:
        for y in range(board.HEIGHT):
            for x in range(board.WIDTH):
                px = OX + x * CELL
                py = OY + y * CELL
                cid = board.get(x, y)
                color = COLORS[TetrominoType(cid)] if cid else _EMPTY
                pygame.draw.rect(self._screen, color,
                                 (px + 1, py + 1, CELL - 2, CELL - 2))
        pygame.draw.rect(self._screen, _GRID,
                         (OX, OY, board.WIDTH * CELL, board.HEIGHT * CELL), 1)

    def _draw_piece(self, piece: Tetromino, alpha: int) -> None:
        for bx, by in piece.get_cells():
            if by < 0:
                continue
            px = OX + bx * CELL
            py = OY + by * CELL
            self._screen.blit(self._cell_surf(piece.color, alpha),
                              (px + 1, py + 1))

    def _draw_ghost(self, board: Board, piece: Tetromino) -> None:
        gy = board.ghost_y(piece)
        if gy == piece.y:
            return
        ghost = piece.copy()
        ghost.y = gy
        for bx, by in ghost.get_cells():
            if by < 0:
                continue
            px = OX + bx * CELL
            py = OY + by * CELL
            self._screen.blit(self._cell_surf(piece.color, _GHOST_A),
                              (px + 1, py + 1))

    def _draw_panel(self, sm: ScoreManager, next_piece: Tetromino) -> None:
        pygame.draw.rect(self._screen, _PANEL_BG,
                         (PANEL_X, OY, WIN_W - PANEL_X - 10,
                          Board.HEIGHT * CELL), border_radius=4)
        cy = OY + 10
        cy = self._label("NEXT",  cy)
        cy = self._draw_next(next_piece, cy) + 8
        cy = self._label("SCORE", cy)
        cy = self._value(str(sm.score), cy) + 8
        cy = self._label("LEVEL", cy)
        cy = self._value(str(sm.level), cy) + 8
        cy = self._label("LINES", cy)
        self._value(str(sm.lines), cy)

    def _draw_next(self, piece: Tetromino, top_y: int) -> int:
        mini = 18
        for row in range(4):
            for col in range(4):
                if piece.shape[row][col]:
                    px = PANEL_X + 10 + col * mini
                    py = top_y + row * mini
                    self._screen.blit(
                        self._cell_surf(piece.color, 255, size=mini - 2),
                        (px, py))
        return top_y + 4 * mini + 4

    def _draw_overlay(self, title: str, subtitle: str) -> None:
        ov = pygame.Surface(self._screen.get_size(), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 150))
        self._screen.blit(ov, (0, 0))
        cx = self._screen.get_width() // 2
        cy = self._screen.get_height() // 2
        self._blit_center(self._font_lg.render(title,    True, _YELLOW), cx, cy - 18)
        self._blit_center(self._font_sm.render(subtitle, True, _WHITE),  cx, cy + 18)

    def _draw_game_over(self, sm: ScoreManager) -> None:
        ov = pygame.Surface(self._screen.get_size(), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 165))
        self._screen.blit(ov, (0, 0))
        cx = self._screen.get_width() // 2
        cy = self._screen.get_height() // 2
        items = [
            (self._font_lg, "GAME OVER",                _YELLOW, cy - 55),
            (self._font_sm, f"SCORE  {sm.score}",       _WHITE,  cy -  5),
            (self._font_sm, f"LEVEL  {sm.level}",       _WHITE,  cy + 22),
            (self._font_sm, f"LINES  {sm.lines}",       _WHITE,  cy + 49),
            (self._font_sm, "R: restart   Q: quit",     _LABEL,  cy + 85),
        ]
        for font, text, color, y in items:
            self._blit_center(font.render(text, True, color), cx, y)

    # ── helpers ─────────────────────────────────────────────────────────

    def _label(self, text: str, y: int) -> int:
        surf = self._font_sm.render(text, True, _LABEL)
        self._screen.blit(surf, (PANEL_X + 10, y))
        return y + surf.get_height() + 2

    def _value(self, text: str, y: int) -> int:
        surf = self._font_lg.render(text, True, _WHITE)
        self._screen.blit(surf, (PANEL_X + 10, y))
        return y + surf.get_height() + 4

    def _blit_center(self, surf: pygame.Surface, cx: int, cy: int) -> None:
        self._screen.blit(surf, surf.get_rect(center=(cx, cy)))

    @staticmethod
    def _cell_surf(color: tuple[int, int, int], alpha: int,
                   size: int = CELL - 2) -> pygame.Surface:
        r, g, b = color
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        surf.fill((r, g, b, alpha))
        hi = (min(r + 60, 255), min(g + 60, 255), min(b + 60, 255), alpha)
        pygame.draw.line(surf, hi, (0, 0), (size - 1, 0))
        pygame.draw.line(surf, hi, (0, 0), (0, size - 1))
        return surf
