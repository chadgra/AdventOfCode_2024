import argparse
from collections import namedtuple
import math
from time import sleep

DAY=15
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

class Map:
    def __init__(self):
        self.guard = None
        self.map = {}
        self.moves = []
        self.width = 0
        self.height = 0

    def add_line(self, line, is_double=False):
        r = self.height
        if line.startswith("#"):
            # map
            if is_double:
                self.width = 2 * len(line)
            else:
                self.width = len(line)
            for c, chr in enumerate(list(line)):
                if chr == "@":
                    if is_double:
                        self.guard = Coord(r, 2 * c)
                        self.map[Coord(r, 2 * c)] = "@"
                    else:
                        self.guard = Coord(r, c)
                        self.map[Coord(r, c)] = chr
                elif chr == "#":
                    if is_double:
                        self.map[Coord(r, 2 * c)] = "#"
                        self.map[Coord(r, 2 * c + 1)] = "#"
                    else:
                        self.map[Coord(r, c)] = chr
                elif chr == "O":
                    if is_double:
                        self.map[Coord(r, 2 * c)] = "["
                        self.map[Coord(r, 2 * c + 1)] = "]"
                    else:
                        self.map[Coord(r, c)] = chr

            self.height += 1
        else:
            # moves
            self.moves += list(line)

    def new_coord(self, coord, move):
        new = None
        match move:
            case "^":
                new = Coord(coord.r - 1, coord.c)
            case "v":
                new = Coord(coord.r + 1, coord.c)
            case "<":
                new = Coord(coord.r, coord.c - 1)
            case ">":
                new = Coord(coord.r, coord.c + 1)
        return new

    def one_move(self, move):
        new = self.guard
        new_g = None
        old_b = None
        while True:
            new = self.new_coord(new, move)
            
            if not new_g:
                new_g = new

            if new not in self.map:
                # open spot
                if old_b:
                    self.map[new] = "O"
                    del self.map[new_g]
                del self.map[self.guard]
                self.guard = new_g
                self.map[self.guard] = "@"
                return
            elif self.map[new] == "O":
                if not old_b:
                    old_b = new
            elif self.map[new] == "#":
                # wall, no moving
                return

    def move_direction(self, coord, dir, perform, chr=None):
        if coord not in self.map:
            if perform:
                self.map[coord] = chr
            return True

        item = self.map[coord]
        if perform:
            del self.map[coord]
        match item:
            case "#":
                return False
            case "@":
                new = self.new_coord(coord, dir)
                possible = self.move_direction(new, dir, perform, item)
            case "[":
                if dir == "<" or dir == ">":
                    new = self.new_coord(coord, dir)
                    possible = self.move_direction(new, dir, perform, item)
                else:
                    left = self.new_coord(coord, dir)
                    right = self.new_coord(coord, ">")
                    right_item = self.map[right]
                    if perform:
                        del self.map[right]
                    right = self.new_coord(right, dir)
                    possible = self.move_direction(left, dir, perform, item) and \
                           self.move_direction(right, dir, perform, right_item)
            case "]":
                if dir == "<" or dir == ">":
                    new = self.new_coord(coord, dir)
                    possible = self.move_direction(new, dir, perform, item)
                else:
                    right = self.new_coord(coord, dir)
                    left = self.new_coord(coord, "<")
                    left_item = self.map[left]
                    if perform:
                        del self.map[left]
                    left = self.new_coord(left, dir)
                    possible = self.move_direction(left, dir, perform, left_item) and \
                           self.move_direction(right, dir, perform, item)
        if perform and chr:
            self.map[coord] = chr
        return possible


    def one_double_move(self, move):
        if self.move_direction(self.guard, move, False):
            # print("possible")
            self.move_direction(self.guard, move, True)
            self.guard = self.new_coord(self.guard, move)
        else:
            # print("not possible")
            pass

    def all_moves(self, is_double=False):
        for move in self.moves:
            if is_double:
                self.one_double_move(move)
                # print()
                # print(move)
                # self.print()
                # sleep(0.01)
            else:
                self.one_move(move)

    def gps_sum(self):
        sum = 0
        for coord, item in self.map.items():
            if item == "O" or item == "[":
                sum += (coord.r * 100) + coord.c
        print(f"gps sum: {sum}")
        return sum

    def print(self):
        for r in range(self.height):
            line = ""
            for c in range(self.width):
                chr = " " if Coord(r, c) not in self.map else self.map[Coord(r, c)]
                line += chr
            print(line)

def get_map(is_double=False):
    map = Map()
    for line in next_line(input_file):
        map.add_line(line.strip(), is_double)
    return map

def do_part_1():
    map = get_map()
    map.all_moves()
    map.print()
    map.gps_sum()

def do_part_2():
    map = get_map(True)
    map.all_moves(True)
    map.print()
    map.gps_sum()

do_part_1()
do_part_2()
