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

input_file = f"input_{DAY:02}.txt"
if not args.full:
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
        self.visited_states = set()
        self.visited_coords = {}

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
                chr = " " if Coord(r, c) not in self.map else self.map[Coord(r, c)]
                line += chr
            print(line)

    def traverse_map(self, coord, dir, steps, turns):
        if coord == self.end:
            # we are at the end, so remember this path
            self.solutions.add(Solution(steps, turns))
            return
        
        # state = State(coord, dir)
        # if state in self.visited_states:
        #     # we've already been here facing this direction, so return
        #     return
        
        if coord in self.visited_coords:
            prev_solution = self.visited_coords[coord]
            prev_score = prev_solution.steps + (prev_solution.turns * 1000)
            cur_score = steps + (turns * 1000)
            if prev_score < cur_score:
                return
        
        # print(f"at {coord} facing {dir} after {steps} steps and {turns} turns")
        if coord in self.map and self.map[coord] == "#":
            # this is a wall, so return
            return
        
        # remember this state
        # self.visited_states.add(state)
        self.visited_coords[coord] = Solution(steps, turns)
        self.traverse_map(dir.next_step(coord), dir, steps + 1, turns)
        cw = dir.next_turn_cw()
        self.traverse_map(cw.next_step(coord), cw, steps + 1, turns + 1)
        cw = cw.next_turn_cw()
        self.traverse_map(cw.next_step(coord), cw, steps + 1, turns + 2)
        ccw = dir.next_turn_ccw()
        self.traverse_map(ccw.next_step(coord), ccw, steps + 1, turns + 1)

    def get_best_solution(self):
        self.traverse_map(self.start, Dir.EAST, 0, 0)

        min_score = 999999999999999999999999999999
        for solution in self.solutions:
            score = solution.steps + (1000 * solution.turns)
            # print(solution)
            # print(score)
            min_score = min(min_score, score)
        print(f"Best score: {min_score}")


def get_map(is_double=False):
    map = Map()
    for line in next_line(input_file):
        map.add_line(line.strip(), is_double)
    return map

def do_part_1():
    map = get_map()
    map.print()
    map.get_best_solution()

def do_part_2():
    return
    map = get_map(True)
    map.print()

do_part_1()
do_part_2()
