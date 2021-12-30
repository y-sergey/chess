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
    Display.print_col_indices()
    for row in range(Board.ROWS - 1, -1, -1):
      print(row + 1, end=' ')
      for col in range(Board.COLS):
        piece = self._board.get_piece(row, col)
        code = ' ' if piece is None else _UNICODES[piece.name()][piece.color()]
        print(code, end='')
      print()
    Display.print_col_indices()
    print()

  @staticmethod
  def print_col_indices():
    print('  ', end='')
    for col in range(0, 8):
      print(chr(ord('A') + col), end='')
    print()
