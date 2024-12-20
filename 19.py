import argparse
from enum import Enum
import functools
import math
from time import sleep
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(20000)  # Set the new limit

DAY=19
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

class Onsen:
    def __init__(self):
        self.patterns = {}
        self.max_pattern_length = 0
        self.designs = []

    def add_line(self, line):
        if "," in line:
            patterns = line.split(", ")
            for pattern in patterns:
                self.patterns[pattern] = True
                self.max_pattern_length = max(self.max_pattern_length, len(pattern))
        elif line:
            self.designs.append(line)

    def print(self):
        print(self.patterns)
        print(self.designs)

    @functools.lru_cache(maxsize=1000)
    def can_make_design(self, design):
        # print(f"Can {design} be made")
        if not design:
            # print(f"We made it!!!!")
            return 1

        # max_chunk = min(self.max_pattern_length, len(design) + 1)
        ways_to_make = 0
        for i in range(1, len(design) + 1):
            # print(f"Try to find {design[:i]}")
            if design[:i] in self.patterns and self.patterns[design[:i]]:
                made_count = self.can_make_design(design[i:])
                ways_to_make += made_count
                # if made_count > 0:
                #     self.patterns[design[i:]] = True
                # else:
                #     self.patterns[design[i:]] = False

        return ways_to_make

    def possible_designs(self):
        checked = 0
        made = 0
        all_different_ways = 0
        for design in self.designs:
            checked += 1
            all_different_ways += self.can_make_design(design)
            print(f"Of {checked} checked found {all_different_ways} ways")
        print(f"{all_different_ways} possibilities")

def get_onsen():
    onsen = Onsen()
    for line in next_line(input_file):
        onsen.add_line(line.strip())
    return onsen

def do_part_1():
    onsen = get_onsen()
    # onsen.print()
    onsen.possible_designs()

def do_part_2():
    onsen = get_onsen()
    onsen.print()

do_part_1()
# do_part_2()
