import argparse
from enum import Enum
import functools
import math
from time import sleep
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(100)  # Set the new limit

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

class LanParty(HashableObject):
    def __init__(self, members):
        super().__init__()
        assert(3 == len(members))
        members.sort()
        self.a = members.pop(0)
        self.b = members.pop(0)
        self.c = members.pop(0)

    def __str__(self):
        return f"\n{self.a.name},{self.b.name},{self.c.name}"

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
                    # It's a party
                    lan_parties.add(LanParty([i, j, k]))
        return lan_parties

class Network:
    def __init__(self):
        self.computers = {}
        self.lan_parties = set()

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

    def find_lan_parties(self):
        for computer in self.computers.values():
            self.lan_parties.update(computer.get_lan_parties())
        # print(self.lan_parties)

    def count_lan_parties_with_t(self):
        count = 0
        for lan_party in self.lan_parties:
            if lan_party.a.name.startswith("t") or \
               lan_party.b.name.startswith("t") or \
               lan_party.c.name.startswith("t"):
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
    pass

do_part_1()
# do_part_2()
