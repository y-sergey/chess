from chess.game.piece import Piece
from chess.game.bishop import Bishop
from chess.game.king import King
from chess.game.knight import Knight
from chess.game.pawn import Pawn
from chess.game.queen import Queen
from chess.game.rook import Rook


class Board:
    ROWS = 8
    COLS = 8

    def __init__(self):
        self._pieces = [[None for _ in range(8)] for _ in range(8)]
        # Pawns
        for col in range(8):
            self._pieces[1][col] = Pawn(Piece.WHITE)
            self._pieces[6][col] = Pawn(Piece.BLACK)

        for row, color in ((0, Piece.WHITE), (7, Piece.BLACK)):
            # Rooks
            for col in (0, 7):
                self._pieces[row][col] = Rook(color)
            # Knights
            for col in (1, 6):
                self._pieces[row][col] = Knight(color)
            # Bishops
            for col in (2, 5):
                self._pieces[row][col] = Bishop(color)
            # Queen
            self._pieces[row][3] = Queen(color)
            # King
            self._pieces[row][4] = King(color)

    def get_piece(self, row, col):
        return self._pieces[row][col]

    def move(self, pos_from: str, pos_to: str):
        from_row = Board.get_row(pos_from)
        from_col = Board.get_col(pos_from)
        to_row = Board.get_row(pos_to)
        to_col = Board.get_col(pos_to)
        piece = self.get_piece(from_row, from_col)
        self._pieces[from_row][from_col] = None
        self._pieces[to_row][to_col] = piece

    @staticmethod
    def get_col(pos):
        return ord(pos[0].lower()) - ord('a')

    @staticmethod
    def get_row(pos):
        return int(pos[1]) - 1
