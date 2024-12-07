import argparse
import copy
from enum import Enum

DAY=6
parser = argparse.ArgumentParser(description=f"Run day {DAY} of Advent of Code")
parser.add_argument("-f", "--full", action="store_true", help="Run against the full input, not just the test input (default)")
args = parser.parse_args()

input_file = f"input_{DAY:02}.txt"
if not args.full:
    input_file = "test_" + input_file

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def next(self):
        if self == Direction.LEFT:
            return Direction.UP
        else:
            return Direction(self.value + 1)

    def turn(self):
        self = self.next()

    def symbol(self):
        match self:
            case Direction.UP:
                return "^"
            case Direction.RIGHT:
                return ">"
            case Direction.DOWN:
                return "v"
            case Direction.LEFT:
                return "<"

class Position:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def symbol(self):
        return map[self.y][self.x]

    def symbol_set(self, symbol):
        map[self.y][self.x] = symbol

    def next(self, direction):
        match direction:
            case Direction.UP:
                return Position(self.x, self.y - 1)
            case Direction.RIGHT:
                return Position(self.x + 1, self.y)
            case Direction.DOWN:
                return Position(self.x, self.y + 1)
            case Direction.LEFT:
                return Position(self.x - 1, self.y)

    def next_symbol(self, direction):
        new_position = self.next(direction)
        return map[new_position.y][new_position.x]

    def step(self, direction):
        new_position = self.next(direction)
        self.x, self.y = new_position.x, new_position.y
        if not 0 <= self.x < len(map[self.y]):
            raise IndexError
        if not 0 <= self.y < len(map):
            raise IndexError
        

    def could_cause_loop(self, direction):
        # if the current position, or any position in that direction
        # has already been visited with this direction then it could
        # cause a loop
        symbol = direction.symbol()
        match direction:
            case Direction.UP:
                y = self.y
                while y >= 0:
                    new_symbol = map[y][self.x]
                    if new_symbol == symbol:
                        return True
                    if new_symbol == "#":
                        return False
                    y -= 1

            case Direction.RIGHT:
                x = self.x
                while x < len(map[self.y]):
                    new_symbol = map[self.y][x]
                    if new_symbol == symbol:
                        return True
                    if new_symbol == "#":
                        return False
                    x += 1

            case Direction.DOWN:
                y = self.y
                while y < len(map):
                    new_symbol = map[y][self.x]
                    if new_symbol == symbol:
                        return True
                    if new_symbol == "#":
                        return False
                    y += 1

            case Direction.LEFT:
                x = self.x
                while x >= 0:
                    new_symbol = map[self.y][x]
                    if new_symbol == symbol:
                        return True
                    if new_symbol == "#":
                        return False
                    x -= 1

        return False

    def print(self):
        print(f"x: {self.x} y: {self.y}")

map = []
guard_location = None
direction = Direction.UP

def next_line(file):
    with open(file, "r") as f:
        for line in f:
            yield line.strip()

line_generator = next_line(input_file)

def populate_map():
    global guard_location
    for y, line in enumerate(line_generator):
        map.append(list(line))
        x = line.find("^")
        if -1 != x:
            guard_location = Position(x, y)

def print_map():
    global guard_location
    guard_location.print()
    for line in map:
        print("".join(line))

def traverse_map_part_1():
    global direction
    global guard_location
    while True:
        try:
            next_symbol = guard_location.next_symbol(direction)
            if "#" == next_symbol:
                # obstacle so turn
                direction = direction.next()
            else:
                #step
                guard_location.symbol_set("X")
                guard_location.step(direction)
        except IndexError:
            # the next step leaves the map so we are done
            guard_location.symbol_set("X")
            break

    position_visited = "".join(["".join(line) for line in map]).count("X")
    print(f"positions visited: {position_visited}")

def would_be_stuck_in_loop(gl, direct):
    times_through_loop = 0
    while True:
        try:
            next_symbol = gl.next_symbol(direct)
            if "#" == next_symbol:
                # obstacle so turn
                direct = direct.next()
            elif direct.symbol() == next_symbol:
                # Already been here going this direction, must be a loop
                return True
            else:
                #step
                times_through_loop += 1
                gl.symbol_set(direct.symbol())
                gl.step(direct)
        except IndexError:
            # the next step leaves the map so we are done
            gl.symbol_set(direct.symbol())
            break
        if times_through_loop > 4 * len(map) * len(map[0]):
            # we've been going around too long - this must be a loop
            return True

    return False

def traverse_map_part_2():
    global map
    global direction
    global guard_location
    loop_point = 0

    while True:
        try:
            next_symbol = guard_location.next_symbol(direction)
            if "#" == next_symbol:
                # obstacle so turn
                direction = direction.next()
            else:
                if "." == next_symbol:
                    # if a turn could create a loop then this is a loop point
                    # make a copy of the map to restore
                    backup_map = copy.deepcopy(map)
                    backup_guard_location = copy.deepcopy(guard_location)
                    backup_direction = copy.deepcopy(direction)
                    # place a obstacle
                    guard_location.next(direction).symbol_set("#")
                    if would_be_stuck_in_loop(guard_location, direction):
                        loop_point += 1
                    map = backup_map
                    guard_location = backup_guard_location
                    direction = backup_direction
                #step
                guard_location.symbol_set(direction.symbol())
                guard_location.step(direction)
        except IndexError:
            # the next step leaves the map so we are done
            guard_location.symbol_set("X")
            break

    print(f"loop points: {loop_point}")

def do_part_1():
    populate_map()
    traverse_map_part_1()

def do_part_2():
    map = []
    populate_map()
    traverse_map_part_2()
    # print_map()

# do_part_1()
do_part_2()
