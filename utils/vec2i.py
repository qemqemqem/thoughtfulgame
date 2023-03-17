from __future__ import annotations


class Vec2i:
    def __init__(self, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y

    def add(self, other: Vec2i):
        return Vec2i(self.x + other.x, self.y + other.y)

    def sub(self, other: Vec2i):
        return Vec2i(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"Vec2i({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    # Define adder
    def __add__(self, other: Vec2i):
        return self.add(other)

    # Define subtractor
    def __sub__(self, other: Vec2i):
        return self.sub(other)
