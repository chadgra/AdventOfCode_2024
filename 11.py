import argparse
from collections import namedtuple

DAY=11
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

class StoneDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set(self, stone, count):
        self[stone] = count

    def add(self, stone, count):
        if stone in self:
            self[stone] += count
        else:
            self[stone] = count

class StoneLine:
    def __init__(self, line) -> None:
        self.line = line
        self.stones = StoneDict()

        for stone in line.split(" "):
            self.stones.add(stone, 1)

    def blink(self):
        new_stones = StoneDict()
        for stone, count in self.stones.items():
            if stone == "0":
                new_stones.add("1", count)
            elif len(stone) % 2 == 0:
                chr_num = int(len(stone) / 2) 
                new_stones.add(stone[:chr_num], count)
                new_stones.add(str(int(stone[chr_num:])), count)
            else:
                new_stones.add(str(int(stone) * 2024), count)
        self.stones = new_stones

    def do_blinks(self, count):
        for i in range(count):
            self.blink()
        
        total_stones = 0
        for _, count in self.stones.items():
            total_stones += count
        
        print(f"total stones: {total_stones}")

def get_stone_line():
    stone_line = None
    for line in next_line(input_file):
        stone_line = StoneLine(line.strip())
    return stone_line

def do_part_1():
    stone_line = get_stone_line()
    stone_line.do_blinks(25)

def do_part_2():
    stone_line = get_stone_line()
    stone_line.do_blinks(75)

do_part_1()
do_part_2()
