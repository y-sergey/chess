from dataclasses import dataclass
from enum import Enum
from enum import unique
from typing import List

import itertools

from chess.game.board import Board
from chess.game.color import Color
from chess.game.move import Move
from chess.game.piece import Piece
from chess.game.square import Square


@unique
class Result(Enum):
    CHECKMATE = 1
    STALEMATE = 2


@dataclass
class State:
    is_check: bool
    result: Result
    turn: Color


class Game:
    def __init__(self):
        self._board = Board()
        self._turn = Color.WHITE
        self._is_check = False
        self._result = None
        self._moves = []
        self._states = []

    def board(self) -> Board:
        return self._board

    def current_player(self) -> Color:
        return self._turn

    def validate_and_move(self, src: Square, dst: Square, pawn_promotion: Piece = None) -> bool:
        piece = self._board.get_piece_by_square(src)
        target_piece = self._board.get_piece_by_square(dst)

        if piece is None:
            return False
        if piece.color() != self._turn:
            return False
        if target_piece is not None and target_piece.color() == self._turn:
            return False
        if not piece.can_move(src, dst, self._board, pawn_promotion):
            return False
        if pawn_promotion and piece.name() != Piece.PAWN:
            return False

        move = Move(
            source=src,
            dest=dst,
            piece=piece,
            captured=target_piece,
            pawn_promotion_piece=pawn_promotion)
        self._apply_move(move)
        if not self._is_last_move_valid(self._turn, move, self._is_check):
            self._undo_move()
            return False
        self._save_game_state()
        self._update_game_state(move)
        return True

    def move(self, move: Move) -> None:
        self._apply_move(move)
        self._save_game_state()
        self._update_game_state(move)

    def undo_move(self) -> None:
        self._undo_move()
        self._restore_game_state()

    def _update_game_state(self, move: Move) -> None:
        next_player = self._turn.opposite()
        self._is_check = self._is_check_after_move(next_player, move)
        opponent_has_valid_moves = self._has_valid_moves(next_player)
        if not opponent_has_valid_moves:
            self._result = Result.CHECKMATE if self._is_check else Result.STALEMATE
        else:
            self._result = None
        self._turn = next_player

    def _save_game_state(self):
        state = State(self._is_check, self._result, self._turn)
        self._states.append(state)

    def _restore_game_state(self):
        state = self._states.pop()
        self._is_check = state.is_check
        self._result = state.result
        self._turn = state.turn

    def _apply_move(self, move: Move) -> None:
        piece = move.piece
        piece.increment_moves()
        dest_piece = move.pawn_promotion_piece if move.pawn_promotion_piece else move.piece
        self._board.remove_piece(move.source)
        self._board.set_piece(move.dest, dest_piece)

        if piece.name() == Piece.KING and piece.is_castle_move(move.source, move.dest):
            rook_square = piece.get_castle_rook_square(move.dest)
            rook = self.board().get_piece_by_square(rook_square)
            target_rook_square = piece.get_target_castle_rook_square(move.dest)
            self._board.remove_piece(rook_square)
            self._board.set_piece(target_rook_square, rook)

        self._moves.append(move)

    def _undo_move(self) -> None:
        move = self._moves.pop()
        piece = move.piece
        piece.decrement_moves()
        self._board.set_piece(move.source, move.piece)
        self._board.set_piece(move.dest, move.captured)

        if piece.name() == Piece.KING and piece.is_castle_move(move.source, move.dest):
            rook_square = piece.get_castle_rook_square(move.dest)
            target_rook_square = piece.get_target_castle_rook_square(move.dest)
            rook = self.board().get_piece_by_square(target_rook_square)
            self._board.remove_piece(target_rook_square)
            self._board.set_piece(rook_square, rook)

    def _is_last_move_valid(self, color: Color, move: Move, is_check: bool) -> bool:
        king_square = self._board.get_king_square(color)
        if move.piece.name() == Piece.KING or is_check:
            for square, piece in self._board.get_pieces_by_color(color.opposite()):
                if piece.threatens(square, king_square, self._board):
                    return False
            return True
        else:
            king = self._board.get_piece_by_square(king_square)
            return not king.is_threatened_on_line(king_square, move.source, self._board)

    def _is_check_after_move(self, color: Color, move: Move) -> bool:
        king_square = self._board.get_king_square(color)
        king = self._board.get_piece_by_square(king_square)
        moved_square = move.dest
        moved_piece = self._board.get_piece_by_square(moved_square)
        return (moved_piece.threatens(moved_square, king_square, self._board)
                or king.is_threatened_on_line(king_square, move.source, self._board))

    def _has_valid_moves(self, color: Color) -> bool:
        return len(list(itertools.islice(self.get_available_moves(color), 0, 1))) > 0

    def get_current_moves(self):
        return list(self._moves)

    def get_available_moves(self, color: Color) -> List[Move]:
        is_check = self._is_check
        for square, piece in self._board.get_pieces_by_color(color):
            for move in piece.get_available_moves(square, self._board):
                self._apply_move(move)
                move_valid = self._is_last_move_valid(color, move, is_check)
                self._undo_move()
                if move_valid:
                    yield move

    def is_check(self) -> bool:
        return self._is_check

    def result(self) -> Result:
        return self._result
