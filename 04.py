import re

# input_file = "test_input_04.txt"
input_file = "input_04.txt"

max_x = 0
horizontal = []
vertical = []
diag_forward = []
diag_backward = []

def next_line(file):
    with open(file, "r") as f:
        for line in f:
            yield line.strip()

line_generator = next_line(input_file)

def split_line_among_indexes(line, table, start_i=0):
    for i, c in enumerate(list(line)):
        i += start_i
        if i >= len(table):
            table.append("")
        table[i] += c

def create_tables():
    global max_x
    diag_i = 0
    for line in line_generator:
        max_x = max(max_x, len(line))
        horizontal.append(line)
        split_line_among_indexes(line, vertical)
        split_line_among_indexes(line, diag_backward, diag_i)
        split_line_among_indexes(line[::-1], diag_forward, diag_i)
        diag_i += 1

def count_xmas():
    count = 0
    count += count_xmas_in_table(horizontal)
    count += count_xmas_in_table(vertical)
    count += count_xmas_in_table(diag_backward)
    count += count_xmas_in_table(diag_forward)
    print(f"xmas count = {count}")

def count_mas():
    count = 0
    positions_back = position_mas_in_table(diag_backward, False)
    positions_for = position_mas_in_table(diag_forward, True)
    for position_back in positions_back:
        if position_back in positions_for:
            count += 1
    print(f"mas count = {count}")

def count_xmas_in_table(table):
    count = 0
    for line in table:
        count += line.count("XMAS")
        count += line.count("SAMX")
    return count

def position_mas_in_table(table, forward):
    positions = []
    for x, line in enumerate(table):
        occurrances = position_mas_in_diag_line(line)
        for occurrance in occurrances:
            positions.append(diag_position_to_cartesian_position(x, occurrance, forward))
    return positions

def diag_position_to_cartesian_position(x, y, forward):
    cart_x, cart_y = x, y
    if x >= max_x:
        diff = x - (max_x - 1)
        cart_x -= diff
        cart_y += diff
    cart_x -= y

    if forward:
        cart_x = (max_x - 1) - cart_x

    return (cart_x, cart_y)

        
def position_mas_in_diag_line(line):
    occurrences = []
    occurrences += position_text_in_diag_line(line, "MAS")
    occurrences += position_text_in_diag_line(line, "SAM")
    occurrences.sort()
    return occurrences

def position_text_in_diag_line(line, text):
    start = 0
    occurrences = []
    while True:
        index = line.find(text, start)
        if index == -1:
            break
        occurrences.append(index + 1)
        start = index + 1
    return occurrences


def print_tables():
    print(f"horizontal:")
    print(f"{horizontal}")
    print(f"vertical:")
    print(f"{vertical}")
    print(f"diag_backward:")
    print(f"{diag_backward}")
    print(f"diag_forward:")
    print(f"{diag_forward}")

create_tables()
count_xmas()
count_mas()
