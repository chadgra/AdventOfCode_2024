#input_file = "test_input_01.txt"
input_file = "input_01.txt"

group_a_location_ids = []
group_b_location_ids = []

def input_file_to_lists(input_file):
    with open(input_file, "r") as input:
        while True:
            line = input.readline()
            if not line:
                break
            a, b = line.split()
            group_a_location_ids.append(int(a))
            group_b_location_ids.append(int(b))

def total_distance():
    group_a_location_ids.sort()
    group_b_location_ids.sort()

    total_distance = 0
    for i in range(len(group_a_location_ids)):
        distance = abs(group_a_location_ids[i] - group_b_location_ids[i])
        # print(f"{i}: {group_a_location_ids[i]} - {group_b_location_ids[i]} = {distance}")
        total_distance += distance
    
    print(f"total distance = {total_distance}")

def similarity():
    group_b_location_ids_map = {}
    for loc_id in group_b_location_ids:
        if loc_id in group_b_location_ids_map:
            group_b_location_ids_map[loc_id] += 1
        else:
            group_b_location_ids_map[loc_id] = 1

    # print(group_b_location_ids_map)

    total_similarity = 0
    for loc_id in group_a_location_ids:
        if loc_id in group_b_location_ids_map:
            total_similarity += (loc_id * group_b_location_ids_map[loc_id])

    print(f"similarity = {total_similarity}")

input_file_to_lists(input_file)
total_distance()
similarity()
