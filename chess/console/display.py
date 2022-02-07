import chess.game.constants as constants
from chess.game.board import Board
from chess.game.color import Color
from chess.game.piece import Piece
from chess.game.square import Square

# Black and white piece colors are swapped
# to work correctly on black-and-white console.
_UNICODES = {
    Piece.PAWN: {
        Color.BLACK: chr(0x2659),
        Color.WHITE: chr(0x265F)
    },
    Piece.ROOK: {
        Color.BLACK: chr(0x2656),
        Color.WHITE: chr(0x265C)
    },
    Piece.KNIGHT: {
        Color.BLACK: chr(0x2658),
        Color.WHITE: chr(0x265E)
    },
    Piece.BISHOP: {
        Color.BLACK: chr(0x2657),
        Color.WHITE: chr(0x265D)
    },
    Piece.KING: {
        Color.BLACK: chr(0x2654),
        Color.WHITE: chr(0x265A)
    },
    Piece.QUEEN: {
        Color.BLACK: chr(0x2655),
        Color.WHITE: chr(0x265B)
    }
}


class Display:

    def __init__(self, board: Board):
        self._board = board

    def show(self):
        print()
        Display._print_col_indices()
        for row in range(constants.NUM_RANKS - 1, -1, -1):
            print(row + 1, end=' ')
            for col in range(constants.NUM_FILES):
                square = Square(rank=row, file=col)
                piece = self._board.get_piece(square)
                code = Display._get_square(row, col) if piece is None else _UNICODES[piece.name()][piece.color()]
                print(code, end=' ')
            print(row + 1)
        Display._print_col_indices()
        print()

    @staticmethod
    def _get_square(row, col):
        return ' ' if (row + col) % 2 == 0 else chr(0x00B7)

    @staticmethod
    def _print_col_indices():
        print('  ', end='')
        for col in range(constants.NUM_FILES):
            print(chr(ord('A') + col), end=' ')
        print()
