from typing import List

import math
import time

from chess.game.color import Color
from chess.game.constants import GamePhase
from chess.game.game import Game
from chess.game.game import Result
from chess.game.move import Move

_CHECKMATE_ADVANTAGE = 500


class MiniMaxBot:

    def __init__(self, color: Color, game: Game):
        self._color = color
        self._game = game
        self._processed_moves = 0
        self._processed_combinations = 0

    def color(self) -> Color:
        return self._color

    def move(self) -> Move:
        self._processed_moves = 0
        self._processed_combinations = 0
        start_time_ns = time.perf_counter_ns()

        depth = 4
        max_advantage, best_move = self._run_minimax(self.color(), depth, None, -math.inf, math.inf)
        assert best_move is not None

        end_time_ns = time.perf_counter_ns()
        elapsed_ns = end_time_ns - start_time_ns
        moves_per_sec = self._processed_moves / elapsed_ns * 10 ** 9
        combinations_per_sec = self._processed_combinations / elapsed_ns * 10 ** 9
        print(f'Elapsed seconds - {elapsed_ns / 10 ** 9}')
        print(f'Moves processed - {self._processed_moves}')
        print(f'Combinations processed - {self._processed_combinations}')
        print(f'Moves per seconds - {moves_per_sec}')
        print(f'Combinations per seconds - {combinations_per_sec}')
        return best_move

    def _run_minimax(self, color: Color, depth: int, last_move: Move, alpha, beta) -> float:
        if depth == 0:
            for move in self._get_moves_to_evaluate(color):
                if self._move(move):
                    self._undo_move()
                    self._processed_combinations = self._processed_combinations + 1
                    advantage = self._evaluate(self._color)
                    return advantage, last_move
            # No valid moves
            if self._game.is_check_after_move(color, last_move):
                # Checkmate
                # print("   CHECKMATE")
                # print(self._game.board().to_string())
                advantage = (
                    -_CHECKMATE_ADVANTAGE if color == self._color
                    else _CHECKMATE_ADVANTAGE)
                return advantage, last_move
            else:
                # Stalemate
                return 0, last_move

        max_advantage = -math.inf
        best_move = None
        moved_made = 0
        for move in self._get_moves_to_evaluate(color):
            move_success = self._move_and_record(move)
            if move_success:
                moved_made += 1
                advantage, _ = self._run_minimax(color.opposite(), depth - 1, move, -beta, -alpha)
                advantage = -advantage
                self._undo_move()
                if advantage > max_advantage:
                    max_advantage = advantage
                    best_move = move
                if advantage >= beta:
                    break
                alpha = max(alpha, max_advantage)

        # Current player doesn't have legal moves
        # This is either a checkmate or a stalemate
        if moved_made == 0:
            if self._game.is_check_after_move(color, last_move):
                advantage = (
                    -_CHECKMATE_ADVANTAGE if color == self._color
                    else _CHECKMATE_ADVANTAGE)
                return advantage, last_move
            else:
                return 0, last_move

        return max_advantage, best_move

    def _evaluate(self, color: Color) -> int:
        scores = [0, 0]
        for square, piece in self._game.board().get_all_pieces():
            idx = piece.color().value
            scores[idx] += piece.material_value() + piece.position_value(square, GamePhase.MIDDLE_GAME)
        return scores[color.value] - scores[color.opposite().value]

    def _move_and_record(self, move: Move) -> bool:
        success = self._move(move)
        if success:
            self._processed_moves = self._processed_moves + 1
        return success

    def _move(self, move: Move) -> bool:
        return self._game.try_move(move)

    def _undo_move(self):
        self._game.undo_move()

    def _get_moves_to_evaluate(self, color: Color) -> List[Move]:
        moves = list()
        for square, piece in self._game.board().get_pieces_by_color(color):
            for move in piece.get_available_moves(square, self._game.board()):
                moves.append(move)
        # Consider moves that capture a piece first
        moves.sort(key=lambda m: m.captured is None)
        return moves
