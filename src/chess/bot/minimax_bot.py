from typing import List

import math
import time

from chess.game.color import Color
from chess.game.constants import GamePhase
from chess.game.game import Game
from chess.game.game import Result
from chess.game.move import Move
from chess.game.piece import Piece

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
        if self._game.result() == Result.STALEMATE:
            return 0, last_move
        if self._game.result() == Result.CHECKMATE:
            advantage = (
                -_CHECKMATE_ADVANTAGE if self._game.current_player() == color
                else _CHECKMATE_ADVANTAGE)
            return advantage, last_move
        if depth == 0:
            # print(self._game.get_current_moves())
            self._processed_combinations = self._processed_combinations + 1
            advantage = self._evaluate(color)
            return advantage, last_move

        if self._game.current_player() == color:
            max_advantage = -math.inf
            best_move = None
            for move in self._get_moves_to_evaluate(color):
                move_success = self._move(move)
                assert move_success
                advantage, _ = self._run_minimax(color, depth - 1, move, alpha, beta)
                self._game.undo_move()
                if advantage > max_advantage:
                    max_advantage = advantage
                    best_move = move
                if advantage >= beta:
                    break
                alpha = max(alpha, advantage)
            return max_advantage, best_move
        else:
            min_advantage = math.inf
            best_move = None
            for move in self._get_moves_to_evaluate(color.opposite()):
                move_success = self._move(move)
                assert move_success
                advantage, _ = self._run_minimax(color, depth - 1, move, alpha, beta)
                self._game.undo_move()
                if advantage < min_advantage:
                    min_advantage = advantage
                    best_move = None
                if advantage <= alpha:
                    break
                beta = min(beta, advantage)
            return min_advantage, best_move

    def _evaluate(self, color: Color) -> int:
        opponent = color.opposite()
        score = 0
        opponent_score = 0
        has_queen = False
        opponent_has_queen = False
        king = None
        opponent_king = None

        for square, piece in self._game.board().get_pieces_by_color(color):
            has_queen = has_queen or piece.name() == Piece.QUEEN
            score += piece.material_value()
            if piece.name() != Piece.KING:
                score += piece.position_value(square, GamePhase.MIDDLE_GAME)
            else:
                king = piece

        for square, piece in self._game.board().get_pieces_by_color(opponent):
            opponent_has_queen = opponent_has_queen or piece.name() == Piece.QUEEN
            opponent_score += piece.material_value()
            if piece.name() != Piece.KING:
                opponent_score += piece.position_value(square, GamePhase.MIDDLE_GAME)
            else:
                opponent_king = piece

        is_end_game = not has_queen and not opponent_has_queen
        phase = GamePhase.END_GAME if is_end_game else GamePhase.MIDDLE_GAME

        score += king.position_value(square, phase)
        opponent_score += opponent_king.position_value(square, phase)

        return score - opponent_score

    def _move(self, move: Move) -> bool:
        self._processed_moves = self._processed_moves + 1
        self._game.move(move)
        return True

    def _get_moves_to_evaluate(self, color: Color) -> List[Move]:
        moves = list(self._game.get_available_moves(color))
        # Consider moves that capture a piece first
        moves.sort(key=lambda move: move.captured is None)
        return moves
