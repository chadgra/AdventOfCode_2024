import re

# input_file = "test_input_05.txt"
input_file = "input_05.txt"

rules = {}
updates = []

def next_line(file):
    with open(file, "r") as f:
        for line in f:
            yield line.strip()

line_generator = next_line(input_file)

def populate_rules_and_updates():
    for line in line_generator:
        if '|' in line:
            a, b = list(map(int, line.split('|')))
            rules[(a, b)] = True
            rules[(b, a)] = False
        elif ',' in line:
            updates.append(list(map(int, line.split(','))))

def valid_updates_total():
    sum = 0
    for update in updates:
        if check_update(update):
            pass
            # sum += update[int(len(update) / 2)]
        else:
            print(f"try and fix this one")
            sum += fix_update(update)
    print(f"sum: {sum}")

def check_update(update):
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            if (update[i], update[j]) in rules:
                if not rules[(update[i], update[j])]:
                    return False
    return True

def fix_update(update):
    while True:
        new_update = swap_two_bad_values_in_update(update)
        if type(new_update) == int:
            return new_update

def swap_two_bad_values_in_update(update):
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            if (update[i], update[j]) in rules:
                if not rules[(update[i], update[j])]:
                    temp = update[i]
                    update[i] = update[j]
                    update[j] = temp
                    return update
    return update[int(len(update) / 2)]


populate_rules_and_updates()
valid_updates_total()
