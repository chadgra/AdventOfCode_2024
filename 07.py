import argparse

DAY=7
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

def concat_numbers(val1, val2):
    res = int(str(val1) + str(val2))
    # print(res)
    return res

def recursive_calc(target, running_calculation, values, with_concat=False):
    # print(f"target: {target} running_calculation: {running_calculation} values: {values}")
    if running_calculation > target:
        return False
    if not values:
        return target == running_calculation

    next_value = values.pop(0)
    solution = recursive_calc(target, running_calculation + next_value, values.copy(), with_concat) or \
        recursive_calc(target, running_calculation * next_value, values.copy(), with_concat)
    if with_concat:
        solution = solution or recursive_calc(target, concat_numbers(running_calculation, next_value), values.copy(), with_concat)

    return solution

class Calibration:
    def __init__(self, line) -> None:
        divided_by_colon = line.split(":")
        self.test_value = int(divided_by_colon[0])
        self.values = list(map(int, divided_by_colon[1].strip().split(' ')))

    def is_possible(self, with_concat=False):
        return recursive_calc(self.test_value, self.values.pop(0), self.values, with_concat)

    def print(self):
        print(f"test_value: {self.test_value} values: {self.values}")

def get_calib_list():
    calib_list = []
    for y, line in enumerate(next_line(input_file)):
        calib_list.append(Calibration(line))
    return calib_list

def print_calib_list(calib_list):
    for calib in calib_list:
        calib.print()

def sum_correct_calib(calib_list, with_concat=False):
    sum = 0
    for calib in calib_list:
        # calib.print()
        if calib.is_possible(with_concat):
            # print("yup, possible")
            sum += calib.test_value
    return sum

def do_part_1():
    calib_list = get_calib_list()
    # print_calib_list(calib_list)
    print(f"sum: {sum_correct_calib(calib_list)}")

def do_part_2():
    calib_list = get_calib_list()
    # print_calib_list(calib_list)
    print(f"sum: {sum_correct_calib(calib_list, True)}")

do_part_1()
do_part_2()
