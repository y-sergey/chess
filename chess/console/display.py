from chess.game.board import Board
from chess.game.piece import Piece

# Black and white piece colors are swapped
# to work correctly on black-and-white console.
_UNICODES = {
    Piece.PAWN: {
        Piece.BLACK: chr(0x2659),
        Piece.WHITE: chr(0x265F)
    },
    Piece.ROOK: {
        Piece.BLACK: chr(0x2656),
        Piece.WHITE: chr(0x265C)
    },
    Piece.KNIGHT: {
        Piece.BLACK: chr(0x2658),
        Piece.WHITE: chr(0x265E)
    },
    Piece.BISHOP: {
        Piece.BLACK: chr(0x2657),
        Piece.WHITE: chr(0x265D)
    },
    Piece.KING: {
        Piece.BLACK: chr(0x2654),
        Piece.WHITE: chr(0x265A)
    },
    Piece.QUEEN: {
        Piece.BLACK: chr(0x2655),
        Piece.WHITE: chr(0x265B)
    }
}


class Display:

    def __init__(self, board: Board):
        self._board = board

    def show(self):
        print()
        Display._print_col_indices()
        for row in range(Board.ROWS - 1, -1, -1):
            print(row + 1, end=' ')
            for col in range(Board.COLS):
                piece = self._board.get_piece(row, col)
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
        for col in range(Board.COLS):
            print(chr(ord('A') + col), end=' ')
        print()
