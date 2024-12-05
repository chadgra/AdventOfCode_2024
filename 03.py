import re

# input_file = "test_input_03.txt"
input_file = "input_03.txt"

def next_line(file):
    with open(file, "r") as f:
        for line in f:
            yield line.strip()

line_generator = next_line(input_file)

def sum_all_muls():
    total = 0
    do = True
    for line in line_generator:
        matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do)\(\)|(don't)\(\)", line)
        for match in matches:
            if match[2] == "do":
                do = True
            elif match[3] == "don't":
                do = False
            elif do:
                total += int(match[0]) * int(match[1])

    print(f"total multiplication = {total}")

sum_all_muls()
