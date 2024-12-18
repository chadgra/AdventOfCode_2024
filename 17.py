import argparse
from enum import Enum
import math
from time import sleep
import sys

DAY=17
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
        for k, v in enumerate(self.__dict__):
            pass
        return (self.attr_a, self.attr_b, self.attr_c)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, A):
            return self.__key() == other.__key()
        return NotImplemented

class Computer:
    def __init__(self):
        self.a = int(0)
        self.b = int(0)
        self.c = int(0)
        self.ip = int(0)
        self.jump = False
        self.program = []
        self.result = []

        self.final_a = 0
        self.ip_jump_at = 0
        self.ip_jump_to = 0
        self.no_more_output = False

    def add_line(self, line):
        if "Register A:" in line:
            self.a = int(line.split(": ")[1])
        elif "Register B:" in line:
            self.b = int(line.split(": ")[1])
        elif "Register C:" in line:
            self.c = int(line.split(": ")[1])
        elif "Program:" in line:
            self.program = line.split(": ")[1]
            self.program = list(map(int, self.program.split(",")))

    def run_program(self, a=None):
        if a:
            self.a = a
        try:
            while True:
                inst, op = self.program[self.ip], self.program[self.ip + 1]
                match inst:
                    case 0:
                        self.adv(op)
                    case 1:
                        self.bxl(op)
                    case 2:
                        self.bst(op)
                    case 3:
                        self.jnz(op)
                    case 4:
                        self.bxc(op)
                    case 5:
                        self.out(op)
                    case 6:
                        self.bdv(op)
                    case 7:
                        self.cdv(op)

                # print()
                # print(f"after {inst}, {op}")
                # self.print()

                if self.jump:
                    self.jump = False
                    continue
                else:
                    self.ip += 2
        except IndexError:
            # return
            print(",".join(str(num) for num in self.result))


    def run_program_backwards_2(self):
        result = self.program.copy()
        self.recursive_backwards(0, result, [])

    def recursive_backwards(self, a, result, current):
        print(f"{current}")
        if not result:
            print(f"This A should work!: {a}")
            return

        b_target = result.pop()
        # print(f"b_target: {b_target}")
        b_target ^= 4
        for i in range(8):
            b = i ^ 1
            test_a = a << 3
            test_a += i
            b = b ^ (test_a >> b)
            # print(f"i: {i} b_target: {b_target} vs b: {b % 8}")
            if b_target == (b % 8):
                new_a = a << 3
                new_a += i
                self.recursive_backwards(new_a, result.copy(), current.copy() + [i])

    def run_program_backwards(self, final_a, final_b, final_c):
        self.final_a = final_a
        self.a = 0
        self.b = final_b
        self.c = final_c
        self.ip = len(self.program) - 2
        self.result = self.program.copy()
        try:
            while True:
                inst, op = self.program[self.ip], self.program[self.ip + 1]
                match inst:
                    case 0:
                        self.adv_inv(op)
                    case 1:
                        self.bxl_inv(op)
                    case 2:
                        self.bst_inv(op)
                    case 3:
                        self.jnz_inv(op)
                    case 4:
                        self.bxc_inv(op)
                    case 5:
                        self.out_inv(op)
                    case 6:
                        self.bdv_inv(op)
                    case 7:
                        self.cdv_inv(op)

                print()
                print(f"after {inst}, {op}")
                self.print()

                if self.ip_jump_at == self.ip and not self.no_more_output:
                    self.ip = self.ip_jump_to
                    continue
                else:
                    self.ip -= 2
        except IndexError:
            return
            print(",".join(str(num) for num in self.result))

    def result_matches_program(self):
        if len(self.program) != len(self.result):
            return False
        for i in range(len(self.program)):
            if self.program[i] != self.result[i]:
                return False
        return True

    def find_correct_a_input(self):
        a = 0
        b = self.b
        c = self.c
        while True:
            # print(f"initial a of {a}")
            self.a = a
            self.b = b
            self.c = c
            self.ip = int(0)
            self.jump = False
            self.result = []
            self.run_program()
            if self.result_matches_program():
                print(f"initial A of {a} recreates the program")
                break
            a += 1

    def combo(self, op):
        if 0 <= op <= 3:
            return op
        elif op == 4:
            return self.a
        elif op == 5:
            return self.b
        elif op == 6:
            return self.c
        else:
            raise Exception("Bad combo value")

    def adv(self, op):
        self.a = int(self.a / (2 ** self.combo(op)))

    def adv_inv(self, op):
        if self.a:
            self.a = int(self.a * (2 ** self.combo(op)))
        else:
            self.a = self.final_a

    def bxl(self, op):
        self.b = int(self.b ^ op)

    def bxl_inv(self, op):
        self.b = int(self.b ^ op)

    def bst(self, op):
        self.b = int(self.combo(op) % 8)

    def bst_inv(self, op):
        b = self.b % 8
        if op == 4:
            self.a = (self.a & ~0x7) + b
        elif op == 5:
            self.b = (self.b & ~0x7) + b
        elif op == 6:
            self.c = (self.c & ~0x7) + b

    def jnz(self, op):
        if not self.a:
            return
        self.jump = True
        self.ip = op

    def jnz_inv(self, op):
        self.ip_jump_to = self.ip
        self.ip_jump_at = op

    def bxc(self, op):
        self.b = int(self.b ^ self.c)

    def bxc_inv(self, op):
        self.b = int(self.b ^ self.c)

    def out(self, op):
        self.result.append(int(self.combo(op) % 8))

    def out_inv(self, op):
        val = self.result.pop()
        if op == 4:
            self.a = (self.a & ~0x7) + val
        if op == 5:
            self.b = (self.b & ~0x7) + val
        if op == 6:
            self.c = (self.c & ~0x7) + val
        
        if not self.result:
            self.no_more_output = True

    def bdv(self, op):
        self.b = int(self.a / (2 ** self.combo(op)))

    def bdv_inv(self, op):
        self.a = int(self.b * (2 ** self.combo(op)))

    def cdv(self, op):
        self.c = int(self.a / (2 ** self.combo(op)))

    def cdv_inv(self, op):
        self.a = int(self.c * (2 ** self.combo(op)))

    def print(self):
        print(f"A: {self.a}")
        print(f"B: {self.b}")
        print(f"C: {self.c}")
        print(f"Program: {self.program}")


def get_computer(is_double=False):
    computer = Computer()
    for line in next_line(input_file):
        computer.add_line(line.strip())
    return computer

def do_part_1():
    computer = get_computer()
    computer.print()
    computer.run_program(a=202991746427434)

def do_part_2():
    computer = get_computer()
    computer.run_program_backwards_2()
    computer.print()

do_part_1()
do_part_2()
