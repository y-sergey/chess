from enum import Enum
from enum import unique

NUM_RANKS = 8
NUM_FILES = 8


class Rank:
    R1 = 0
    R2 = 1
    R3 = 2
    R4 = 3
    R5 = 4
    R6 = 5
    R7 = 6
    R8 = 7

    @staticmethod
    def is_valid(rank: int) -> bool:
        return Rank.R1 <= rank <= Rank.R8

    @staticmethod
    def mirror(rank: int) -> int:
        return 7 - rank


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


@unique
class GamePhase(Enum):
    OPENING = 1
    MIDDLE_GAME = 2
    END_GAME = 3
