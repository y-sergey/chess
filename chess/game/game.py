from chess.game.board import Board
from chess.game.color import Color
from chess.game.move import Move
from chess.game.piece import Piece
from chess.game.square import Square


class Game:
    def __init__(self):
        self._board = Board()
        self._turn = Color.WHITE
        self._is_check = False
        self._moves = []

    def board(self) -> Board:
        return self._board

    def current_player(self) -> Color:
        return self._turn

    def move(self, src: Square, dst: Square, pawn_promotion: Piece = None) -> bool:
        piece = self._board.get_piece(src)
        target_piece = self._board.get_piece(dst)

        if piece is None:
            return False
        if piece.color() != self._turn:
            return False
        if target_piece is not None and target_piece.color() == self._turn:
            return False
        if not piece.can_move(src, dst, self._board):
            return False

        move = Move(
            source=src,
            dest=dst,
            piece=piece,
            captured=target_piece,
            pawn_promotion_piece=pawn_promotion)
        self._apply_move(move)
        if self._is_king_in_check(self._turn):
            self._undo_move()
            return False

        next_player = self._turn.opposite()
        self._is_check = self._is_king_in_check(next_player)
        self._turn = next_player

        return True

    def _apply_move(self, move: Move):
        dest_piece = move.pawn_promotion_piece if move.pawn_promotion_piece else move.piece
        self._board.remove_piece(move.source)
        self._board.set_piece(move.dest, dest_piece)
        self._moves.append(move)

    def _undo_move(self):
        move = self._moves.pop()
        self._board.set_piece(move.source, move.piece)
        self._board.set_piece(move.dest, move.captured)

    def _is_king_in_check(self, color: Color) -> bool:
        king_square = self._board.get_king_square(color)
        for piece, square in self._board.get_pieces_by_color(color.opposite()):
            if piece.threatens(square, king_square, self._board):
                return True
        return False

    def is_check(self):
        return self._is_check
