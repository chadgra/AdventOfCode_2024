import argparse
from enum import Enum
import functools
import math
from time import sleep
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(2000)  # Set the new limit

DAY=23
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
            try:
                hash(v)
                val_list.append(v)
            except TypeError:
                pass
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

class Computer(HashableObject):
    def __init__(self, name):
        self.name = name
        self.connections = set()

    def __str__(self):
        connection_names = ""
        for connection in self.connections:
            connection_names += f"{connection.name}, "
        return f"{self.name}: {connection_names}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.name < other.name

    def get_lan_parties(self):
        lan_parties = set()
        i = self
        for j in self.connections:
            for k in i.connections:
                if (i in j.connections) and (i in k.connections) and \
                   (j in i.connections) and (j in k.connections) and \
                   (k in i.connections) and (k in j.connections):
                    # It's a party!!
                    name = [i.name, j.name, k.name]
                    name.sort()
                    lan_parties.add(",".join(name))
        return lan_parties

class Network:
    def __init__(self):
        self.computers = {}
        self.lan_parties = set()
        self.size_of_each_party = 0
        self.connection_count_map = {}

    def add_line(self, line):
        computers = []
        for computer_name in line.split("-"):
            if computer_name in self.computers:
                computer = self.computers[computer_name]
            else:
                computer = Computer(computer_name)
                self.computers[computer_name] = computer
            computers.append(computer)

        computers[0].connections.add(computers[1])
        computers[1].connections.add(computers[0])

    def print(self):
        print(self.computers)

    def lan_party_name_to_members(self, name):
        members = []
        for member_name in name.split(","):
            members.append(self.computers[member_name])
        return members

    def lan_party_party_members_to_name(self, members, exclude=[]):
        member_names = []
        for member in members:
            if member not in exclude:
                member_names.append(member.name)
        member_names.sort()
        return ",".join(member_names)

    def find_lan_parties(self):
        self.size_of_each_party = 3
        for computer in self.computers.values():
            self.lan_parties.update(computer.get_lan_parties())
        # print(self.lan_parties)

    def increase_lan_party_size(self):
        bigger_parties = set()
        for party in self.lan_parties:
            party_members = self.lan_party_name_to_members(party)
            for party_member in party_members:
                for connection in party_member.connections:
                    if connection not in party_members:
                        potential_party = self.lan_party_party_members_to_name(party_members + [connection], [party_member])
                        if potential_party in self.lan_parties:
                            bigger_parties.add(self.lan_party_party_members_to_name(party_members + [connection]))

        self.size_of_each_party += 1
        self.lan_parties = bigger_parties        

    def find_connection_count(self):
        for computer in self.computers.values():
            num_connections = len(computer.connections)
            self.connection_count_map[num_connections] = self.connection_count_map.get(num_connections, 0) + 1
        print(self.connection_count_map)

    def find_largest_connected_component(self):
        visited = set()
        max_size = 0

        def dfs(computer):
            visited.add(computer)
            current_size = 1
            for neighbor in computer.connections:
                if neighbor not in visited:
                    current_size += dfs(neighbor)
            return current_size

        for computer in self.computers.values():
            if computer not in visited:
                current_component_size = dfs(computer)
                max_size = max(max_size, current_component_size)

        print(f"largest connected component: {max_size}")
        return max_size

    def count_lan_parties_with_t(self):
        count = 0
        for lan_party in self.lan_parties:
            members = lan_party.split(",")
            if members[0].startswith("t") or \
               members[1].startswith("t") or \
               members[2].startswith("t"):
                count += 1
        print(f"{count} parties have a computer that starts with t")
        return count

def next_line(file):
    with open(file, "r") as f:
        for line in f:
            yield line.strip()

def get_network():
    network = Network()
    for line in next_line(input_file):
        network.add_line(line.strip())
    return network

def do_part_1():
    network = get_network()
    # network.print()
    network.find_lan_parties()
    network.count_lan_parties_with_t()

def do_part_2():
    network = get_network()
    network.find_lan_parties()
    print(f"{len(network.lan_parties)} with {network.size_of_each_party} members")
    while len(network.lan_parties) > 1:
        network.increase_lan_party_size()
        print(f"{len(network.lan_parties)} with {network.size_of_each_party} members")

    print(network.lan_parties)
    # network.find_connection_count()
    # network.find_largest_connected_component()

# do_part_1()
do_part_2()
