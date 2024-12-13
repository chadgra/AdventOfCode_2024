import argparse
from collections import namedtuple
import math

DAY=13
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

Coordinate = namedtuple("Coordinate", ["r", "c"])
Side = namedtuple("Side", ["r", "c", "horizontal"])

class Button:
    def __init__(self, line):
        self.line = line
        line_list = line.replace("+", ", ").split(", ")
        self.x = int(line_list[1])
        self.y = int(line_list[3])

class Prize:
    def __init__(self, line):
        self.line = line
        line_list = line.replace("=", ", ").split(", ")
        self.x = int(line_list[1]) + 10000000000000
        self.y = int(line_list[3]) + 10000000000000

class Equation:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def slope(self):
        return -1 * (self.a / self.b)

    def intercept(self):
        return self.c / self.b

    def solve_for_b(self, a):
        return (self.slope() * a) + self.intercept()

    def is_whole_press_solution(self, a_presses, b_presses):
        return (round(a_presses) * self.a) + (round(b_presses) * self.b) == self.c

class EquationSystem:
    def __init__(self, eq1, eq2):
        self.eq1 = eq1
        self.eq2 = eq2
        self.a_presses = float(0)
        self.b_presses = float(0)

    def solve(self):
        if self.eq1.slope() != self.eq2.slope():
            return self.solve_simple()
        elif self.eq1.intercept() != self.eq2.intercept():
            return None
        else:
            return self.solve_optimized()

    def solve_simple(self):
        self.a_presses = (self.eq2.intercept() - self.eq1.intercept()) / (self.eq1.slope() - self.eq2.slope())
        self.b_presses = self.eq1.solve_for_b(self.a_presses)
        print(f"a presses: {self.a_presses} b presses: {self.b_presses}")

    def solve_optimized(self):
        print("can't solve this yet!")
        pass

    def cost(self):
        print(f"eq1 is whole: {self.eq1.is_whole_press_solution(self.a_presses, self.b_presses)}")
        print(f"eq2 is whole: {self.eq2.is_whole_press_solution(self.a_presses, self.b_presses)}")
        if self.eq1.is_whole_press_solution(self.a_presses, self.b_presses) and \
           self.eq2.is_whole_press_solution(self.a_presses, self.b_presses):
            return (3 * round(self.a_presses)) + (1 * round(self.b_presses))
        return 0

class ClawMachine:
    def __init__(self):
        self.button_a = None
        self.button_b = None
        self.prize = None

    def __str__(self):
        text = ""
        text += f"Button A: x+{self.button_a.x}, y+{self.button_a.y}\n"
        text += f"Button B: x+{self.button_b.x}, y+{self.button_b.y}\n"
        text += f"Prize: x={self.prize.x}, y={self.prize.y}\n"
        return text

    def add_line(self, line):
        if "Button A:" in line:
            self.button_a = Button(line)
        elif "Button B:" in line:
            self.button_b = Button(line)
        elif "Prize:" in line:
            self.prize = Prize(line)

    def solve(self):
        eq1 = Equation(self.button_a.x, self.button_b.x, self.prize.x)
        eq2 = Equation(self.button_a.y, self.button_b.y, self.prize.y)

        system = EquationSystem(eq1, eq2)
        system.solve()
        return system.cost()

class Arcade:
    def __init__(self):
        self.machines = [ClawMachine()]

    def add_line(self, line):
        if self.machines:
            machine = self.machines[-1]

        if line == "":
            machine = ClawMachine()
            self.machines.append(machine)

        machine.add_line(line)

    def print(self):
        for machine in self.machines:
            print(machine)
            print()

    def fewest_tokens(self):
        tokens = 0
        for machine in self.machines:
            tokens += machine.solve()
        print(f"{tokens} to win")
        return tokens


def get_arcade():
    arcade = Arcade()
    for line in next_line(input_file):
        arcade.add_line(line.strip())
    return arcade

def do_part_1():
    arcade = get_arcade()
    arcade.print()
    arcade.fewest_tokens()

def do_part_2():
    pass

do_part_1()
do_part_2()
