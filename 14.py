import argparse
from collections import namedtuple
import math

DAY=14
parser = argparse.ArgumentParser(description=f"Run day {DAY} of Advent of Code")
parser.add_argument("-f", "--full", action="store_true", help="Run against the full input, not just the test input (default)")
args = parser.parse_args()

WIDTH=101
HEIGHT=103

input_file = f"input_{DAY:02}.txt"
if not args.full:
    input_file = "test_" + input_file
    WIDTH = 11
    HEIGHT = 7

def next_line(file):
    with open(file, "r") as f:
        for line in f:
            yield line.strip()

Coord = namedtuple("Coord", ["x", "y"])

class Guard:
    def __init__(self, line):
        line_list = line.replace("=", ",").replace(" ", ",").split(",")
        self.x = int(line_list[1])
        self.y = int(line_list[2])
        self.dx = int(line_list[4])
        self.dy = int(line_list[5])

    def __str__(self):
        text = f"P={self.x},{self.y} V={self.dx},{self.dy}\n"
        return text

    def location_after(self, seconds):
        x = self.x + (seconds * self.dx)
        y = self.y + (seconds * self.dy)
        x %= WIDTH
        y %= HEIGHT
        x += WIDTH if x < 0 else 0
        y += HEIGHT if y < 0 else 0
        return (x, y)

class Lobby:
    def __init__(self):
        self.guards = []
        self.quadrants = [
            [0, 0],
            [0, 0]
        ]
        self.guards_set = set()

    def add_line(self, line):
        self.guards.append(Guard(line))

    def print(self):
        for y in range(HEIGHT):
            line = ""
            for x in range(WIDTH):
                chr = "X" if Coord(x, y) in self.guards_set else " "
                line += chr
            print(line)

    def safety_factor(self, seconds):
        for guard in self.guards:
            x, y = guard.location_after(seconds)
            # print(f"{x},{y}")

            if (x == ((WIDTH - 1) / 2)) or (y == ((HEIGHT - 1) / 2)):
                continue
            self.quadrants[math.floor(x / (WIDTH / 2))][math.floor(y / (HEIGHT / 2))] += 1
        
        factor = 1
        for r in self.quadrants:
            for v in r:
                # print(f"v: {v}")
                factor *= v

        print(f"safety factor: {factor}")

    def show_graph(self):
        seconds = 1
        while True:
            self.guards_set = set()
            for guard in self.guards:
                x, y = guard.location_after(seconds)
                self.guards_set.add(Coord(x, y))
            
            if Coord((WIDTH - 1) / 2, 0) in self.guards_set:
                self.print()
                print(f"After {seconds} seconds")
                input("")
            seconds += 1


def get_lobby():
    lobby = Lobby()
    for line in next_line(input_file):
        lobby.add_line(line.strip())
    return lobby

def do_part_1():
    lobby = get_lobby()
    lobby.safety_factor(100)

def do_part_2():
    lobby = get_lobby()
    lobby.show_graph()

# do_part_1()
do_part_2()
