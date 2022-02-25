import math

from chess.game.color import Color
from chess.game.game import Game
from chess.game.game import Result
from chess.game.move import Move

_MOVE_LIMIT = 10


class MiniMaxBot:

    def __init__(self, color: Color, game: Game):
        self._color = color
        self._game = game

    def color(self) -> Color:
        return self._color

    def move(self) -> Move:
        max_advantage = -math.inf
        best_move = None
        for move in self._game.get_available_moves(self._color)[:_MOVE_LIMIT]:
            result = self._game.move(move.source, move.dest, move.pawn_promotion_piece)
            assert result
            advantage = self._run_minimax(self._color, depth=2)
            self._game.undo_move()
            if advantage > max_advantage:
                best_move = move
                max_advantage = advantage
        return best_move

    def _run_minimax(self, color: Color, depth: int) -> float:
        if self._game.result() == Result.STALEMATE:
            return 0
        if self._game.result() == Result.CHECKMATE:
            return -math.inf if self._game.current_player() == color else math.inf
        if depth == 0:
            # print(self._game.get_current_moves())
            return self._game.board().get_material_advantage(color)

        if self._game.current_player() == color:
            max_advantage = -math.inf
            for move in self._game.get_available_moves(color)[:_MOVE_LIMIT]:
                result = self._game.move(move.source, move.dest, move.pawn_promotion_piece)
                assert result
                advantage = self._run_minimax(color, depth - 1)
                self._game.undo_move()
                if advantage > max_advantage:
                    max_advantage = advantage
            return max_advantage
        else:
            min_advantage = math.inf
            for move in self._game.get_available_moves(color.opposite())[:_MOVE_LIMIT]:
                result = self._game.move(move.source, move.dest, move.pawn_promotion_piece)
                assert result
                advantage = self._run_minimax(color, depth - 1)
                self._game.undo_move()
                if advantage < min_advantage:
                    min_advantage = advantage
            return min_advantage
