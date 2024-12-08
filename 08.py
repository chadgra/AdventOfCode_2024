import argparse
from collections import namedtuple

DAY=8
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

class City:
    def __init__(self) -> None:
        self.city_map = []
        self.height = 0
        self.width = 0
        self.frequency_locations = {}
        self.antinodes = set()

    def add_line(self, line):
        line_list = list(line)
        self.width = len(line_list)
        self.city_map.append(line_list)
        r = self.height
        for c, chr in enumerate(line_list):
            if chr != ".":
                if chr in self.frequency_locations:
                    self.frequency_locations[chr].append(Location(r, c))
                else:
                    self.frequency_locations[chr] = [Location(r, c)]
        self.height += 1

    def node_in_bounds(self, node):
        r, c = node
        return 0 <= r < self.height and 0 <= c < self.width

    def get_antinodes(self, node1, node2, with_resonant_harmonics=False):
        dr = node1.r - node2.r
        dc = node1.c - node2.c

        if not with_resonant_harmonics:
            new_antinode_1 = Location(node1.r + dr, node1.c + dc)
            new_antinode_2 = Location(node2.r - dr, node2.c - dc)
            return [new_antinode_1, new_antinode_2]
        
        new_nodes = []
        multiplier = 0
        while True:
            new_antinode_1 = Location(node1.r + (multiplier * dr), node1.c + (multiplier * dc))
            new_antinode_2 = Location(node1.r - (multiplier * dr), node1.c - (multiplier * dc))
            new_nodes.append(new_antinode_1)
            new_nodes.append(new_antinode_2)
            if not self.node_in_bounds(new_antinode_1) and not self.node_in_bounds(new_antinode_2):
                break
            multiplier += 1

        return new_nodes

    def find_antinodes(self, with_resonant_harmonics=False):
        for freq, locations in self.frequency_locations.items():
            for i in range(len(locations)):
                for j in range(i + 1, len(locations)):
                    new_antinodes = self.get_antinodes(self.frequency_locations[freq][i], self.frequency_locations[freq][j], with_resonant_harmonics)
                    for node in new_antinodes:
                        self.antinodes.add((node.r, node.c))

        # remove out of bounds
        filtered = [x for x in set(self.antinodes) if self.node_in_bounds(x)]
        # print(filtered)
        print(len(filtered))


def get_city():
    city = City()
    for line in next_line(input_file):
        city.add_line(line.strip())
    return city

def do_part_1():
    city = get_city()
    city.find_antinodes()

def do_part_2():
    city = get_city()
    city.find_antinodes(True)

do_part_1()
do_part_2()
