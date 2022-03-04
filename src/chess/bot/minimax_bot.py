from typing import List

import math
import time

from chess.game.color import Color
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

        max_advantage = -math.inf
        best_move = None
        depth = 2
        for move in self._get_moves_to_evaluate(self.color()):
            move_success = self._move(move)
            assert move_success
            advantage = self._run_minimax(self._color, depth)
            self._game.undo_move()
            if advantage > max_advantage:
                best_move = move
                max_advantage = advantage

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

    def _run_minimax(self, color: Color, depth: int) -> float:
        if self._game.result() == Result.STALEMATE:
            return 0
        if self._game.result() == Result.CHECKMATE:
            return (
                -_CHECKMATE_ADVANTAGE if self._game.current_player() == color
                else _CHECKMATE_ADVANTAGE)
        if depth == 0:
            # print(self._game.get_current_moves())
            self._processed_combinations = self._processed_combinations + 1
            advantage = self._game.board().get_material_advantage(color)
            return advantage

        if self._game.current_player() == color:
            max_advantage = -math.inf
            for move in self._get_moves_to_evaluate(color):
                move_success = self._move(move)
                assert move_success
                advantage = self._run_minimax(color, depth - 1)
                self._game.undo_move()
                if advantage > max_advantage:
                    max_advantage = advantage
            return max_advantage
        else:
            min_advantage = math.inf
            for move in self._get_moves_to_evaluate(color.opposite()):
                move_success = self._move(move)
                assert move_success
                advantage = self._run_minimax(color, depth - 1)
                self._game.undo_move()
                if advantage < min_advantage:
                    min_advantage = advantage
            return min_advantage

    def _move(self, move: Move) -> bool:
        self._processed_moves = self._processed_moves + 1
        self._game.move(move)
        return True

    def _get_moves_to_evaluate(self, color: Color) -> List[Move]:
        moves = list(self._game.get_available_moves(color))
        # Consider moves that capture a piece first
        moves.sort(key=lambda move: move.captured is None)
        return moves
