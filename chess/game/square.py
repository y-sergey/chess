from dataclasses import dataclass


@dataclass
class Square:
    file: int
    rank: int

    def add_rank(self, steps: int):
        return Square(file=self.file, rank=self.rank + steps)

    def add_file(self, steps: int):
        return Square(file=self.file + steps, rank=self.rank)

    def add_steps(self, file_steps, rank_steps):
        return Square(file=self.file + file_steps, rank=self.rank + rank_steps)

    def __str__(self):
        file_str = chr(ord('A') + self.file)
        return f'{file_str}{self.rank + 1}'
