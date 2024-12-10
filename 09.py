import argparse
from collections import namedtuple

DAY=9
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

SpaceInfo = namedtuple("SpaceInfo", ["index", "size"])

class Disk:
    def __init__(self, line) -> None:
        self.line = list(line)
        self.disk = []
        self.file_map = {}
        self.space_map = {}

        file = True
        file_id = 0
        space_id = 0
        index = 0
        for num in self.line:
            if file:
                self.disk += [file_id] * int(num)
                self.file_map[file_id] = SpaceInfo(index, int(num))
                file_id += 1
            else:
                self.disk += ["."] * int(num)
                self.space_map[space_id] = SpaceInfo(index, int(num))
                space_id += 1
            file = not file
            index += int(num)

        # print(self.disk)

    def clean_disk(self):
        l, r = 0, len(self.disk) - 1
        while True:
            while self.disk[l] != ".":
                l += 1
            while self.disk[r] == ".":
                r -= 1
            if r <= l:
                break
            temp = self.disk[l]
            self.disk[l] = self.disk[r]
            self.disk[r] = temp

        # print(self.disk)

    def clean_disk_optimized(self):
        files = list(self.file_map.keys())
        files.sort(reverse=True)

        spaces = list(self.space_map.keys())
        spaces.sort()

        for file_id in files:
            file_info = self.file_map[file_id]
            # is there space for this file somewhere else:
            for space_id in spaces:
                if space_id > file_id:
                    break
                space_info = self.space_map[space_id]
                if space_info.size >= file_info.size:
                    # there is space for this one so move it:
                    for i in range(space_info.index, space_info.index + file_info.size):
                        self.disk[i] = file_id
                    for i in range(file_info.index, file_info.index + file_info.size):
                        self.disk[i] = "."
                    # also update the info for the space:
                    self.space_map[space_id] = SpaceInfo(space_info.index + file_info.size, space_info.size - file_info.size)
                    break
        
        # print(self.disk)
        
    def disk_checksum(self):
        checksum = 0
        for i, id in enumerate(self.disk):
            if id != ".":
                checksum += i * id
        print(checksum)

def get_disk():
    disk = None
    for line in next_line(input_file):
        disk = Disk(line.strip())
    return disk

def do_part_1():
    disk = get_disk()
    disk.clean_disk()
    disk.disk_checksum()

def do_part_2():
    disk = get_disk()
    disk.clean_disk_optimized()
    disk.disk_checksum()
    # test data should be:
    # 00992111777.44.333....5555.6666.....8888..

do_part_1()
do_part_2()
