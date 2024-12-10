import argparse
from collections import namedtuple

DAY=10
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

Location = namedtuple("Location", ["r", "c"])

class Map:
    def __init__(self) -> None:
        self.width = 0
        self.height = 0
        self.topographic = []
        self.trail_heads = {}

    def add_line(self, line):
        line_list = list(map(int, line))
        self.width = len(line_list)
        self.topographic.append(line_list)
        r = self.height
        for c, chr in enumerate(line_list):
            if chr == 0:
                self.trail_heads[Location(r, c)] = []
        self.height += 1

    def above(self, location):
        if location.r <= 0:
            return None
        return Location(location.r - 1, location.c)
    
    def below(self, location):
        if location.r >= (self.height - 1):
            return None
        return Location(location.r + 1, location.c)
    
    def left(self, location):
        if location.c <= 0:
            return None
        return Location(location.r, location.c - 1)
    
    def right(self, location):
        if location.c >= (self.width - 1):
            return None
        return Location(location.r, location.c + 1)

    def location_height(self, location):
        return self.topographic[location.r][location.c]

    def find_peaks_from_trail(self, trail_head, location):
        location_height = self.location_height(location)
        if location_height == 9:
            self.trail_heads[trail_head].append(location)
            return

        location_height += 1
        # now search in all directions
        steps = [self.above(location), self.below(location), self.left(location), self.right(location)]
        for step in steps:
            if step and self.location_height(step) == location_height:
                self.find_peaks_from_trail(trail_head, step)

    def find_all_trail_head_score(self, all_paths=False):
        for trail_head in self.trail_heads:
            self.find_peaks_from_trail(trail_head, trail_head)
        
        score = 0
        for _, peaks in self.trail_heads.items():
            if not all_paths:
                filtered = list(dict.fromkeys(peaks))
                score += len(filtered)
            else:
                score += len(peaks)
        print(score)
        return score

def get_map():
    map = Map()
    for line in next_line(input_file):
        map.add_line(line.strip())
    return map

def do_part_1():
    map = get_map()
    map.find_all_trail_head_score()

def do_part_2():
    map = get_map()
    map.find_all_trail_head_score(True)

do_part_1()
do_part_2()
