import argparse
from enum import Enum
import math
from time import sleep
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(20000)  # Set the new limit

DAY=18
parser = argparse.ArgumentParser(description=f"Run day {DAY} of Advent of Code")
parser.add_argument("-f", "--full", action="store_true", help="Run against the full input, not just the test input (default)")
args = parser.parse_args()

HEIGHT = 71
WIDTH = 71
MAX_BYTE_COUNT = 1024
input_file = f"input_{DAY:02}.txt"
if not args.full:
    HEIGHT = 7
    WIDTH = 7
    MAX_BYTE_COUNT = 12
    input_file = "test_" + input_file

def next_line(file):
    with open(file, "r") as f:
        for line in f:
            yield line.strip()

class HashableObject:
    def __key(self):
        val_list = []
        for k, v in self.__dict__.items():
            val_list.append(v)
        return tuple(val_list)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, __class__):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return self.__str__()

class Coord(HashableObject):
    def __init__(self, r, c):
        super().__init__()
        self.r = r
        self.c = c

    def get_neighbors(self):
        return [
            Coord(self.r - 1, self.c),
            Coord(self.r + 1, self.c),
            Coord(self.r, self.c - 1),
            Coord(self.r, self.c + 1)
        ]

    def get_valid_neighbors(self, width, height):
        valid = []
        for neighbor in self.get_neighbors():
            if (0 <= neighbor.c < width) and (0 <= neighbor.r < height):
                valid += [neighbor]
        return valid

class Map:
    def __init__(self, max_byte_count):
        self.width = WIDTH
        self.height = HEIGHT
        self.max_byte_count = max_byte_count
        self.obstacles = set()
        self.obstacles_list = []
        self.visited = {}
        self.byte_count = 0
        self.begin = Coord(0, 0)
        self.end = Coord(self.height - 1, self.width - 1)

    def add_line(self, line):
        if self.byte_count >= self.max_byte_count:
            return

        points = list(map(int, line.split(",")))
        coord = Coord(points[1], points[0])
        self.obstacles.add(coord)
        self.obstacles_list.append(coord)
        self.byte_count += 1

    def print(self):
        print(self.obstacles)
        for r in range(self.height):
            row = ""
            for c in range(self.width):
                row += "#" if Coord(r, c) in self.obstacles else "."
            print(row)

    def take_step(self, coord, count):
        # A maximum path would be every cell
        max_path = self.width * self.height

        if coord == self.end:
            # This is the end so return the number of steps that were taken
            return count

        if coord in self.obstacles:
            # This is an obstacle so return a big number
            return max_path

        if coord in self.visited:
            if self.visited[coord] <= count:
                return max_path

        self.visited[coord] = count

        min_path = self.width * self.height
        for neighbor in coord.get_valid_neighbors(self.width, self.height):
            min_path = min(min_path, self.take_step(neighbor, count + 1))
        
        return min_path

def get_map(max_byte_count):
    map = Map(max_byte_count)
    for line in next_line(input_file):
        map.add_line(line.strip())
    return map

def do_part_1():
    map = get_map(MAX_BYTE_COUNT)
    map.print()
    print(f"Min path: {map.take_step(map.begin, 0)}")

def do_part_2():
    # Find first number that causes "self.width * self.height"
    map = get_map(999999999999)
    min = 0
    max = len(map.obstacles)
    while max >= min:
        trial = int((max + min) / 2)
        map = get_map(trial)
        steps = map.take_step(map.begin, 0)
        print(f"trial {trial} took {steps} steps, last point {map.obstacles_list.pop()}")
        if steps == (map.width * map.height):
            # search lower
            max = trial - 1
        else:
            min = trial + 1

# do_part_1()
do_part_2()
