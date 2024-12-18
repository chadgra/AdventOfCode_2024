import argparse
from collections import namedtuple
from enum import Enum
import math
from time import sleep
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(20000)  # Set the new limit

DAY=16
parser = argparse.ArgumentParser(description=f"Run day {DAY} of Advent of Code")
parser.add_argument("-f", "--full", action="store_true", help="Run against the full input, not just the test input (default)")
args = parser.parse_args()

BEST_SOLUTION = 94444
input_file = f"input_{DAY:02}.txt"
if not args.full:
    BEST_SOLUTION = 11048
    input_file = "test_" + input_file

def next_line(file):
    with open(file, "r") as f:
        for line in f:
            yield line.strip()

Coord = namedtuple("Coord", ["r", "c"])
Solution = namedtuple("Solution", ["steps", "turns"])
State = namedtuple("State", ["coord", "dir"])

class Dir(Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    def next_turn_ccw(self):
        if self == Dir.EAST:
            return Dir.NORTH
        else:
            return Dir(self.value - 1)

    def next_turn_cw(self):
        if self == Dir.NORTH:
            return Dir.EAST
        else:
            return Dir(self.value + 1)

    def next_step(self, coord):
        match self:
            case Dir.EAST:
                return Coord(coord.r, coord.c + 1)
            case Dir.SOUTH:
                return Coord(coord.r + 1, coord.c)
            case Dir.WEST:
                return Coord(coord.r, coord.c - 1)
            case Dir.NORTH:
                return Coord(coord.r - 1, coord.c)

def get_score(solution):
    return solution.steps + (solution.turns * 1000)

def increment_solution(solution, steps, turns):
    return Solution(solution.steps + steps, solution.turns + turns)

class Map:
    def __init__(self):
        self.map = {}
        self.position = None
        self.dir = Dir.EAST
        self.start = None
        self.end = None
        self.solutions = set()
        self.width = 0
        self.height = 0
        self.visited_coords = {}
        self.coords_on_best_route = set()

    def add_line(self, line, is_double=False):
        r = self.height
        self.width = len(line)
        if line.startswith("#"):
            # map
            for c, chr in enumerate(list(line)):
                if chr == "S":
                    self.start = Coord(r, c)
                    self.map[Coord(r, c)] = "o"
                elif chr == "E":
                    self.end = Coord(r, c)
                elif chr == "#":
                    self.map[Coord(r, c)] = chr

            self.height += 1

    def print(self):
        print(f"Start: {self.start} End: {self.end}")
        for r in range(self.height):
            line = ""
            for c in range(self.width):
                if Coord(r, c) in self.coords_on_best_route:
                    chr = "O"
                else:
                    chr = " " if Coord(r, c) not in self.map else self.map[Coord(r, c)]
                line += chr
            print(line)

    def traverse_map(self, coord, dir, solution, path):
        if get_score(solution) > BEST_SOLUTION:
            return

        if coord == self.end:
            # we are at the end, so remember this path
            self.solutions.add(solution)
            self.coords_on_best_route.update(path + [coord])
            return

        if coord in self.visited_coords:
            prev_solution = self.visited_coords[coord]
            prev_score = get_score(prev_solution)
            cur_score = get_score(solution)
            if prev_score + 1000 < cur_score:
                return

        # print(f"at {coord} facing {dir} after {steps} steps and {turns} turns")
        if coord in self.map and self.map[coord] == "#":
            # this is a wall, so return
            return
        
        # remember this state
        self.visited_coords[coord] = solution
        self.traverse_map(dir.next_step(coord), dir, increment_solution(solution, 1, 0), path + [coord])
        cw = dir.next_turn_cw()
        self.traverse_map(cw.next_step(coord), cw, increment_solution(solution, 1, 1), path + [coord])
        cw = cw.next_turn_cw()
        self.traverse_map(cw.next_step(coord), cw, increment_solution(solution, 1, 2), path + [coord])
        ccw = dir.next_turn_ccw()
        self.traverse_map(ccw.next_step(coord), ccw, increment_solution(solution, 1, 1), path + [coord])

    def get_best_solution(self):
        self.traverse_map(self.start, Dir.EAST, Solution(0, 0), [self.start])

        min_score = 999999999999999999999999999999
        for solution in self.solutions:
            score = get_score(solution)
            # print(solution)
            # print(score)
            min_score = min(min_score, score)
        print(f"Best score: {min_score}")
        print(f"Coords visited: {len(self.coords_on_best_route)}")


def get_map(is_double=False):
    map = Map()
    for line in next_line(input_file):
        map.add_line(line.strip(), is_double)
    return map

def do_part_1():
    map = get_map()
    map.print()
    map.get_best_solution()
    map.print()

def do_part_2():
    return
    map = get_map(True)
    map.print()

do_part_1()
do_part_2()
