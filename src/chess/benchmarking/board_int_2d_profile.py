import profile

from chess.game.color import Color

piece_scores_map = {
    1: 1,  # pawn
    2: 3,  # knight,
    3: 3,  # bishop
    4: 5,  # rook
    5: 10,  # queen
    6: 10000,  # king
    11: 1,  # pawn
    12: 3,  # knight,
    13: 3,  # bishop
    14: 5,  # rook
    15: 10,  # queen
    16: 10000,  # king
}

piece_scores = [0, 1, 3, 3, 5, 10, 1000, 0, 0, 0, 0, 1, 3, 3, 5, 10, 10000]


class IntBoard:
    def __init__(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        for i in range(8):
            # pawn
            self.board[1][i] = 1
            self.board[6][i] = 11
        # rook
        self.board[0][0] = self.board[0][7] = 4
        self.board[7][0] = self.board[7][7] = 14
        # knight
        self.board[0][1] = self.board[0][6] = 2
        self.board[7][1] = self.board[7][6] = 12
        # bishop
        self.board[0][2] = self.board[0][5] = 3
        self.board[7][2] = self.board[7][5] = 13
        # queen
        self.board[0][3] = 5
        self.board[7][3] = 15
        # king
        self.board[0][4] = 6
        self.board[7][4] = 16


_board = IntBoard()


def _evaluate() -> int:
    color = Color.WHITE
    scores = [0, 0]
    for row in _board.board:
        for val in row:
            idx = val // 10
            score = piece_scores[val]
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
