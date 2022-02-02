from dataclasses import dataclass


@dataclass
class Square:
    file: int
    rank: int

    def add_rank(self, steps: int):
        return Square(file=self.file, rank=self.rank + steps)

    def __str__(self):
        file_str = chr(ord('A') + self.file)
        return f'{file_str}{self.rank + 1}'
