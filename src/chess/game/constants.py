from enum import Enum
from enum import unique

NUM_RANKS = 8
NUM_FILES = 8


@unique
class Rank(Enum):
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
        return Rank.RANK_1.value <= rank <= Rank.RANK_8.value


@unique
class File(Enum):
    FILE_A = 0
    FILE_B = 1
    FILE_C = 2
    FILE_D = 3
    FILE_E = 4
    FILE_F = 5
    FILE_G = 6
    FILE_H = 7

    @staticmethod
    def is_valid(file: int) -> bool:
        return File.FILE_A.value <= file <= File.FILE_H.value
