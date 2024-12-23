import argparse
from enum import Enum
import functools
import math
from time import sleep
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(100)  # Set the new limit

DAY=22
parser = argparse.ArgumentParser(description=f"Run day {DAY} of Advent of Code")
parser.add_argument("-f", "--full", action="store_true", help="Run against the full input, not just the test input (default)")
args = parser.parse_args()

input_file = f"input_{DAY:02}.txt"
if not args.full:
    input_file = "test_" + input_file

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

class Sequence(HashableObject):
    def __init__(self, sequence):
        super().__init__()
        self.a = sequence[0]
        self.b = sequence[1]
        self.c = sequence[2]
        self.d = sequence[3]

class SecretNumber:
    def __init__(self, init):
        self.init = init
        self.val = init
        self.found_sequences = set()

    def mix(self, new_val):
        self.val ^= new_val

    def prune(self):
        self.val %= 16777216

    def next_secret(self):
        first = self.val * 64
        self.mix(first)
        self.prune()

        second = math.floor(self.val / 32)
        self.mix(second)
        self.prune()

        third = self.val * 2048
        self.mix(third)
        self.prune()

    def next_x_secrets(self, x, sequence_map={}):
        changes = []
        last_price = None
        for i in range(x):
            self.next_secret()
            price = self.val % 10
            if last_price != None:
                change = price - last_price
                changes.append(change)
                if len(changes) > 4:
                    changes.pop(0)
                    sequence = Sequence(changes)
                    if sequence not in self.found_sequences:
                        self.found_sequences.add(sequence)
                        if sequence in sequence_map:
                            sequence_map[sequence] += price
                        else:
                            sequence_map[sequence] = price

            last_price = price

def next_line(file):
    with open(file, "r") as f:
        for line in f:
            yield line.strip()

def get_init_numbers():
    init_numbers = []
    for line in next_line(input_file):
        init_numbers.append(int(line.strip()))
    return init_numbers

def do_part_1():
    init_numbers = get_init_numbers()
    sum = 0
    for num in init_numbers:
        secret_number = SecretNumber(num)
        secret_number.next_x_secrets(2000)
        sum += secret_number.val
        # print(secret_number.val)

    print(f"sum of secret numbers: {sum}")

def do_part_2():
    init_numbers = get_init_numbers()
    secret_map = {}
    for num in init_numbers:
        secret_number = SecretNumber(num)
        secret_number.next_x_secrets(2000, secret_map)

    best_price = 0
    best_sequence = None
    for sequence, price in secret_map.items():
        if price > best_price:
            best_price = price
            best_sequence = sequence

    print(f"Best sequence: {best_sequence} with total of {best_price}")

# do_part_1()
do_part_2()
