import argparse
from enum import Enum
import functools
import math
from time import sleep
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(20000)  # Set the new limit

DAY=20
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

    def get_up(self):
        return Coord(self.r - 1, self.c)

    def get_down(self):
        return Coord(self.r + 1, self.c)

    def get_left(self):
        return Coord(self.r, self.c - 1)

    def get_right(self):
        return Coord(self.r, self.c + 1)

    def get_all_coords_steps_away(self, steps):
        all_cords = {}
        for i in range(1, steps + 1):
            for j in range(i + 1):
                all_cords[Coord(self.r + (i - j), self.c + j)] = i
                all_cords[Coord(self.r + (i - j), self.c - j)] = i
                all_cords[Coord(self.r - (i - j), self.c + j)] = i
                all_cords[Coord(self.r - (i - j), self.c - j)] = i
        return all_cords

    def get_steps_from(self, coord):
        return abs(self.r - coord.r) + abs(self.c - coord.c)

    def get_neighbors(self):
        return [
            self.get_up(),
            self.get_down(),
            self.get_left(),
            self.get_right()
        ]

    def get_valid_neighbors(self, width, height):
        valid = []
        for neighbor in self.get_neighbors():
            if (0 <= neighbor.c < width) and (0 <= neighbor.r < height):
                valid += [neighbor]
        return valid

class Cheat(HashableObject):
    def __init__(self, start, stop):
        super().__init__()
        self.start = start
        self.stop = stop

class Map:
    def __init__(self):
        self.walls = set()
        self.start = None
        self.end = None
        self.path = []
        self.path_costs = {}
        self.width = 0
        self.height = 0
        self.cheat_savings = {}

    def add_line(self, line):
        r = self.height
        self.width = len(line)
        for c, chr in enumerate(list(line)):
            if chr == "#":
                self.walls.add(Coord(r, c))
            if chr == "S":
                self.start = Coord(r, c)
            if chr == "E":
                self.end = Coord(r, c)
        self.height += 1

    def print(self):
        for r in range(self.height):
            row = ""
            for c in range(self.width):
                coord = Coord(r, c)
                if coord in self.walls:
                    row += "#"
                elif coord in self.path:
                    row += "o"
                else:
                    row += " "
            print(row)

    def solve_maze_bfs(self, cheat=None):
        queue = [(self.start, [self.start])]
        visited = set()

        while queue:
            current, path = queue.pop(0)

            if current == self.end:
                self.path = path + [current]
                return len(path)

            if current in visited:
                continue

            visited.add(current)

            for neighbor in current.get_valid_neighbors(self.width, self.height):
                if (neighbor not in self.walls) or (cheat and cheat.is_coord(neighbor)):
                    queue.append((neighbor, path + [current]))

        return None

    def find_cheat_options(self, cheat_size=2, threshold=100):
        savings_above_threshold = 0
        self.solve_maze_bfs()
        for step, coord in enumerate(self.path):
            self.path_costs[coord] = step

        print(f"Without cheating it takes {len(self.path_costs) - 1} steps")
        # Go along path looking for shortcuts
        for start_cheat in self.path:
            for stop_cheat, cheat_steps in start_cheat.get_all_coords_steps_away(cheat_size).items():
                if stop_cheat in self.path_costs:
                    savings = self.path_costs[stop_cheat] - ((self.path_costs[start_cheat] + cheat_steps))
                    if savings > 0:
                        # print(f"start: {start_cheat} to {stop_cheat} saves {savings}")
                        if savings not in self.cheat_savings:
                            self.cheat_savings[savings] = set([Cheat(start_cheat, stop_cheat)])
                        else:
                            self.cheat_savings[savings].add(Cheat(start_cheat, stop_cheat))

        sorted_dict = dict(sorted(self.cheat_savings.items(), key=lambda item: item[0]))
        for savings, cheat_set in sorted_dict.items():
            if savings >= threshold:
                savings_above_threshold += len(cheat_set)
                print(f"{len(cheat_set)} cheats save {savings} seconds")
        print(f"{savings_above_threshold} cheats above {threshold}")

def get_map():
    map = Map()
    for line in next_line(input_file):
        map.add_line(line.strip())
    return map

def do_part_1():
    map = get_map()
    map.find_cheat_options(2, 100)

def do_part_2():
    # coord = Coord(3, 3)
    # print(coord.get_all_coords_steps_away(3))
    # print(len(coord.get_all_coords_steps_away(3)))
    map = get_map()
    map.find_cheat_options(20, 100)

# do_part_1()
do_part_2()
