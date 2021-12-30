from chess.game.piece import Piece


class Bishop(Piece):
  def __init__(self, color):
    Piece.__init__(self, Piece.BISHOP, color)
