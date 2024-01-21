
from enum import Enum

class Specs(Enum):
    A0 = (841, 1189)
    A1 = (594, 841)
    A2 = (420, 594)
    A3 = (297, 420)
    A4 = (210, 297)
  

    def __init__(self, width, height):
        self.width = width
        self.height = height

    @staticmethod
    def get_size(paper_type):
        if paper_type in Specs.__members__:
            paper = Specs[paper_type]
            return (paper.width, paper.height)
        else:
            raise ValueError(f"Invalid paper size: {paper_type}")

# Example usage
# print(Specs.A4)  # (210, 297)
# print(Specs.A0)  # (841, 1189)

# A4
# AB/CD, 2 
# 13/46, 3

# A3
# AC/CF , 3
# 14/58, 4

# A2
# AD/EH, 4
# 16/712

# A1
# AF/GM, 6
# 18/916, 8

# A0
# AH/JR, 8
# 112/1324, 12


# 16txt