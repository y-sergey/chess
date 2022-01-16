from dataclasses import dataclass


@dataclass
class Square:
    file: int
    rank: int

    def add_rank(self, steps: int):
        return Square(file=self.file, rank=self.rank + steps)
