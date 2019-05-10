
import math


class Vertex:
    def __init__(self):
        self.weight = 0
        self.distance = math.inf
        self.parent = None