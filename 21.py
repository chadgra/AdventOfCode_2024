import argparse
from enum import Enum
import functools
import math
from time import sleep
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(100)  # Set the new limit

DAY=21
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

brute_force_map = {
    ('A', 'v'): "<vA",
    ('v', '<'): "<A",
    ('<', '<'): "A",
    ('<', 'A'): ">>^A",
    ('A', '<'): "v<<A",
    ('<', 'v'): ">A",
    ('A', '>'): "vA",
    ('>', '>'): "A",
    ('>', '^'): "<^A",
    ('^', 'A'): ">A",
    ('^', '>'): "v>A",
    ('>', 'A'): "^A",
    ('A', '0'): "<A",
    ('A', 'A'): "A",
    ('0', '0'): "A",
    ('v', 'A'): "^>A",
    ('A', '^'): "<A",
    ('0', 'A'): ">A",
    ('<', '^'): ">^A",
    ('^', '<'): "v<A",
    ('>', 'v'): "<A",
    ('v', '>'): ">A",
    ('0', '1'): "^<A",
    ('1', 'A'): ">>vA",
    ('0', '2'): "^A",
    ('2', 'A'): "v>A",
    ('0', '3'): "^>A",
    ('3', 'A'): "vA",
    ('^', '^'): "A",
    ('0', '4'): "^^<A",
    ('v', 'v'): "A",
    ('4', 'A'): ">>vvA",
    ('0', '5'): "^^A",
    ('5', 'A'): "vv>A",
    ('0', '6'): "^^>A",
    ('6', 'A'): "vvA",
    ('0', '7'): "^^^<A",
    ('7', 'A'): ">>vvvA",
    ('0', '8'): "^^^A",
    ('8', 'A'): "vvv>A",
    ('0', '9'): "^^^>A",
    ('9', 'A'): "vvvA",
    ('A', '1'): "^<<A",
    ('1', '0'): ">vA",
    ('1', '1'): "A",
    ('1', '2'): ">A",
    ('1', '3'): ">>A",
    ('1', '4'): "^A",
    ('1', '5'): "^>A",
    ('1', '6'): "^>>A",
    ('1', '7'): "^^A",
    ('1', '8'): "^^>A",
    ('1', '9'): "^^>>A",
    ('A', '2'): "<^A",
    ('2', '0'): "vA",
    ('2', '1'): "<A",
    ('2', '2'): "A",
    ('2', '3'): ">A",
    ('2', '4'): "<^A",
    ('2', '5'): "^A",
    ('2', '6'): "^>A",
    ('2', '7'): "<^^A",
    ('2', '8'): "^^A",
    ('2', '9'): "^^>A",
    ('A', '3'): "^A",
    ('3', '0'): "<vA",
    ('3', '1'): "<<A",
    ('3', '2'): "<A",
    ('3', '3'): "A",
    ('3', '4'): "<<^A",
    ('3', '5'): "<^A",
    ('3', '6'): "^A",
    ('3', '7'): "<<^^A",
    ('3', '8'): "<^^A",
    ('3', '9'): "^^A",
    ('A', '4'): "^^<<A",
    ('4', '0'): ">vvA",
    ('4', '1'): "vA",
    ('4', '2'): "v>A",
    ('4', '3'): "v>>A",
    ('4', '4'): "A",
    ('4', '5'): ">A",
    ('4', '6'): ">>A",
    ('4', '7'): "^A",
    ('4', '8'): "^>A",
    ('4', '9'): "^>>A",
    ('A', '5'): "<^^A",
    ('5', '0'): "vvA",
    ('5', '1'): "<vA",
    ('5', '2'): "vA",
    ('5', '3'): "v>A",
    ('5', '4'): "<A",
    ('5', '5'): "A",
    ('5', '6'): ">A",
    ('5', '7'): "<^A",
    ('5', '8'): "^A",
    ('5', '9'): "^>A",
    ('A', '6'): "^^A",
    ('6', '0'): "<vvA",
    ('6', '1'): "<<vA",
    ('6', '2'): "<vA",
    ('6', '3'): "vA",
    ('6', '4'): "<<A",
    ('6', '5'): "<A",
    ('6', '6'): "A",
    ('6', '7'): "<<^A",
    ('6', '8'): "<^A",
    ('6', '9'): "^A",
    ('A', '7'): "^^^<<A",
    ('7', '0'): ">vvvA",
    ('7', '1'): "vvA",
    ('7', '2'): "vv>A",
    ('7', '3'): "vv>>A",
    ('7', '4'): "vA",
    ('7', '5'): "v>A",
    ('7', '6'): "v>>A",
    ('7', '7'): "A",
    ('7', '8'): ">A",
    ('7', '9'): ">>A",
    ('A', '8'): "<^^^A",
    ('8', '0'): "vvvA",
    ('8', '1'): "<vvA",
    ('8', '2'): "vvA",
    ('8', '3'): "vv>A",
    ('8', '4'): "<vA",
    ('8', '5'): "vA",
    ('8', '6'): "v>A",
    ('8', '7'): "<A",
    ('8', '8'): "A",
    ('8', '9'): ">A",
    ('A', '9'): "^^^A",
    ('9', '0'): "<vvvA",
    ('9', '1'): "<<vvA",
    ('9', '2'): "<vvA",
    ('9', '3'): "vvA",
    ('9', '4'): "<<vA",
    ('9', '5'): "<vA",
    ('9', '6'): "vA",
    ('9', '7'): "<<A",
    ('9', '8'): "<A",
    ('9', '9'): "A"
}

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

    def get_next(self, dir):
        match dir:
            case "^":
                return self.get_up()
            case "v":
                return self.get_down()
            case "<":
                return self.get_left()
            case ">":
                return self.get_right()

    def get_up(self):
        return Coord(self.r - 1, self.c)

    def get_down(self):
        return Coord(self.r + 1, self.c)

    def get_left(self):
        return Coord(self.r, self.c - 1)

    def get_right(self):
        return Coord(self.r, self.c + 1)


class Keypad:
    def __init__(self):
        self.chr_map = {}

        self.width = 0
        self.height = 0
        for r, line in enumerate(self.layout):
            self.width = len(line)
            for c, chr in enumerate(list(line)):
                self.chr_map[chr] = Coord(r, c)
            self.height += 1

    @functools.lru_cache(maxsize=200)
    def get_paths_between_coords(self, a, b, path=""):
        # print(f"entering between cords with {a} and {b} and {path}")
        if a == b:
            return [path + "A"]

        if self.layout[a.r][a.c] == "#":
            # This space is not allowed
            return []
        
        v_diff = a.r - b.r
        h_diff = a.c - b.c

        paths = []
        if v_diff > 0:
            new_path = path + "^"
            paths += self.get_paths_between_coords(a.get_next("^"), b, new_path)
        elif v_diff < 0:
            new_path = path + "v"
            paths += self.get_paths_between_coords(a.get_next("v"), b, new_path)

        if h_diff > 0:
            new_path = path + "<"
            paths += self.get_paths_between_coords(a.get_next("<"), b, new_path)
        elif h_diff < 0:
            new_path = path + ">"
            paths += self.get_paths_between_coords(a.get_next(">"), b, new_path)

        # Filter paths that make unnecessary turns:
        filtered_paths = []
        for path in paths:
            # print(f"considering {path}")
            chr_last_index = {}
            for i, chr in enumerate(list(path)):
                if chr == "A":
                    filtered_paths.append(path)
                if chr in chr_last_index:
                    if chr_last_index[chr] != i - 1:
                        break
                chr_last_index[chr] = i

        # print(f"******for {a} to {b} paths: {filtered_paths}")
        return filtered_paths

    def get_paths_between(self, a, b):
        coord_a = self.chr_map[a]
        coord_b = self.chr_map[b]
        paths = self.get_paths_between_coords(coord_a, coord_b)
        return paths

    def get_paths_for_code(self, code):
        paths = []
        a = "A"
        for b in code:
            combined_paths = []
            new_paths = self.get_paths_between(a, b)
            if paths:
                for path in paths:
                    for new_path in new_paths:
                        combined_paths.append(path + new_path)
                paths = combined_paths
            else:
                paths = new_paths

            a = b
        return paths

    def choose_best_path(self, paths, depth=0):
        # print(paths)
        # print(f"Try to choose best paths from {len(paths)}")
        if len(paths) == 1:
            return paths[0]

        new_path_to_parent_map = {}
        time_to_path_map = {}

        total_paths_found = 0
        for path in paths:
            # print(time_to_path_map.keys())
            new_paths = self.get_paths_for_code(path)
            total_paths_found += len(new_paths)
            for new_path in new_paths:
                new_path_to_parent_map[new_path] = path
                if len(new_path) in time_to_path_map:
                    time_to_path_map[len(new_path)].append(new_path)
                else:
                    time_to_path_map[len(new_path)] = [new_path]

        # Now we have a table of all the paths - if there is one best one then choose that,
        # otherwise see which one of those is best
        min_size = min(time_to_path_map.keys())
        paths = time_to_path_map[min_size]
        parent_path_score = {}
        for path in paths:
            parent_path = new_path_to_parent_map[path]
            if parent_path in parent_path_score:
                parent_path_score[parent_path] += 1
            else:
                parent_path_score[parent_path] = 1

        # print("Parent path score")
        # print(parent_path_score)
        num_at_max = 0
        max_count = max(parent_path_score.values())
        for parent_path, count in parent_path_score.items():
            if count == max_count:
                num_at_max += 1

        if num_at_max == 1 or depth >= 2:
            best_score = 0
            best_path = None
            for path, score in parent_path_score.items():
                if score > best_score:
                    best_score = score
                    best_path = path
            return best_path
        else:
            return new_path_to_parent_map[self.choose_best_path(paths, depth + 1)]

    @functools.lru_cache(maxsize=1000)
    def get_best_path_between_cords(self, a, b):
        global direction
        paths = self.get_paths_between_coords(a, b)
        return direction.choose_best_path(paths)

    def get_best_path_between(self, a, b):
        if (a, b) in brute_force_map:
            return brute_force_map[(a, b)]

        coord_a = self.chr_map[a]
        coord_b = self.chr_map[b]
        path = self.get_best_path_between_cords(coord_a, coord_b)
        return path

    def get_best_path_for_code(self, code):
        path = ""
        a = "A"
        for b in code:
            path += self.get_best_path_between(a, b)
            a = b
        return path

class NumericKeypad(Keypad):
    def __init__(self):
        self.layout = [
            "789",
            "456",
            "123",
            "#0A"
        ]
        super().__init__()

class DirectionKeypad(Keypad):
    def __init__(self):
        self.layout = [
            "#^A",
            "<v>"
        ]
        super().__init__()

class Sequence(HashableObject):
    def __init__(self, queue):
        super().__init__()
        self.a = queue[0]
        self.b = queue[1]

    def code(self):
        return self.a + self.b
    
    def __str__(self):
        return f"{self.a}{self.b}"

numeric = NumericKeypad()
direction = DirectionKeypad()

def code_to_map(code, count=1, map={}):
    split_codes = code.split("A")
    split_codes.pop()
    for split_code in split_codes:
        split_code += "A"
        if split_code in map:
            map[split_code] += count
        else:
            map[split_code] = count
    return map

def map_to_map(map):
    new_map = {}
    for code, count in map.items():
        new_code = direction.get_best_path_for_code(code)
        code_to_map(new_code, count, new_map)
    return new_map

def solve_code(code, direction_count=2):
    path = numeric.get_best_path_for_code(code)
    map = code_to_map(path, 1, {})
    # print(code)
    # print(path)
    # print(map)

    for i in range(direction_count):
        # print(path)
        map = map_to_map(map)
        # print(map)

    seq_length = 0
    for seq, count in map.items():
        seq_length += count * (len(seq))
        # if seq == "A":
        #     seq_length += count
        # else:

    # print(path)
    print(f"length of path: {seq_length} value = {int(code.replace('A', ''))}")
    return seq_length * int(code.replace("A", ""))

def solve_codes(codes, direction_count=2):
    complexity_total = 0
    for code in codes:
        complexity_total += solve_code(code, direction_count)
    
    print(f"Complexity total: {complexity_total}")

def get_codes():
    codes = []
    for line in next_line(input_file):
        codes.append(line.strip())
    return codes

def do_part_1():
    codes = get_codes()
    solve_codes(codes)

def do_part_2():
    codes = get_codes()
    solve_codes(codes, 25)

do_part_1()
do_part_2()
