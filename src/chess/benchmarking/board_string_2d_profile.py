import profile

from chess.game.color import Color

piece_scores_map = {
    '.': 0,
    'p': 1,  # pawn
    'n': 3,  # knight,
    'b': 3,  # bishop
    'r': 5,  # rook
    'q': 10,  # queen
    'k': 10000,  # king
    'P': 1,  # pawn
    'N': 3,  # knight,
    'B': 3,  # bishop
    'R': 5,  # rook
    'Q': 10,  # queen
    'K': 10000,  # king
}


class StringBoard:
    def __init__(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        for i in range(8):
            # pawn
            self.board[1][i] = 'p'
            self.board[6][i] = 'P'
        # rook
        self.board[0][0] = self.board[0][7] = 'r'
        self.board[7][0] = self.board[7][7] = 'R'
        # knight
        self.board[0][1] = self.board[0][6] = 'n'
        self.board[7][1] = self.board[7][6] = 'N'
        # bishop
        self.board[0][2] = self.board[0][5] = 'b'
        self.board[7][2] = self.board[7][5] = 'B'
        # queen
        self.board[0][3] = 'q'
        self.board[7][3] = 'Q'
        # king
        self.board[0][4] = 'k'
        self.board[7][4] = 'K'


_board = StringBoard()


def _evaluate() -> int:
    color = Color.WHITE
    scores = [0, 0]
    for row in _board.board:
        for val in row:
            idx = 0 if val.islower() else 1
            score = piece_scores_map[val]
            scores[idx] += score
    return scores[color.value] - scores[color.opposite().value]


def main():
    for i in range(8):
        for j in range(8):
            print(_board.board[i][j], end=' ')
        print()
    # _evaluate()
    profile.run('for i in range(10000): _evaluate()', sort='cumtime')


if __name__ == '__main__':
    main()
