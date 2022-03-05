NUM_RANKS = 8
NUM_FILES = 8


class Rank:
    RANK_1 = 0
    RANK_2 = 1
    RANK_3 = 2
    RANK_4 = 3
    RANK_5 = 4
    RANK_6 = 5
    RANK_7 = 6
    RANK_8 = 7

    @staticmethod
    def is_valid(rank: int) -> bool:
        return Rank.RANK_1 <= rank <= Rank.RANK_8


class File:
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7

    @staticmethod
    def is_valid(file: int) -> bool:
        return File.A <= file <= File.H
