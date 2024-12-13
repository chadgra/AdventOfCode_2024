import argparse
from collections import namedtuple

DAY=12
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

class Plot:
    def __init__(self, type, coordinate):
        self.type = type
        self.coordinate = coordinate
        self.neighbors_same = set()
        self.neighbors_different = set()
        self.sides_outter = set()
        self.region = None

    def side_between(self, neighbor):
        return Side(float((self.coordinate.r + neighbor.coordinate.r) / 2),
                    float((self.coordinate.c + neighbor.coordinate.c) / 2),
                    (self.coordinate.c == neighbor.coordinate.c))

    def get_neighbor_coordinates(self):
        neighbors = [
            Coordinate(self.coordinate.r - 1, self.coordinate.c),
            Coordinate(self.coordinate.r + 1, self.coordinate.c),
            Coordinate(self.coordinate.r, self.coordinate.c - 1),
            Coordinate(self.coordinate.r, self.coordinate.c + 1),
        ]
        return neighbors

    def get_side_coordinates(self):
        sides = [
            Side(float(self.coordinate.r - 0.5), float(self.coordinate.c), True),
            Side(float(self.coordinate.r + 0.5), float(self.coordinate.c), True),
            Side(float(self.coordinate.r), float(self.coordinate.c - 0.5), False),
            Side(float(self.coordinate.r), float(self.coordinate.c + 0.5), False),
        ]
        return sides

class Region:
    def __init__(self, type):
        self.type = type
        self.plots = set()
        self.sides_outter = set()

    def area(self):
        return len(self.plots)

    def perimeter(self):
        fences = 0
        for plot in self.plots:
            fences += len(plot.sides_outter)
        return fences
    
    def remove_whole_side(self, side):
        # print()
        # print(f"considering side {side}")
        # print(f"from all remaining sides: {self.sides_outter}")
        if side.horizontal:
            back_stoppers = [Side(side.r - 0.5, side.c - 0.5, False),
                             Side(side.r + 0.5, side.c - 0.5, False)]
            fore_stoppers = [Side(side.r - 0.5, side.c + 0.5, False),
                             Side(side.r + 0.5, side.c + 0.5, False)]
            back_piece = Side(side.r, side.c - 1, True)
            fore_piece = Side(side.r, side.c + 1, True)
        else:
            back_stoppers = [Side(side.r - 0.5, side.c - 0.5, True),
                             Side(side.r - 0.5, side.c + 0.5, True)]
            fore_stoppers = [Side(side.r + 0.5, side.c - 0.5, True),
                             Side(side.r + 0.5, side.c + 0.5, True)]
            back_piece = Side(side.r - 1, side.c, False)
            fore_piece = Side(side.r + 1, side.c, False)

        stoppers_present = set()
        back_stopper_present = False
        for back_stopper in back_stoppers:
            if back_stopper in self.sides_outter:
                stoppers_present.add(back_stopper)
                back_stopper_present = True
                break

        fore_stopper_present = False
        for fore_stopper in fore_stoppers:
            if fore_stopper in self.sides_outter:
                stoppers_present.add(fore_stopper)
                fore_stopper_present = True
                break

        self.sides_outter.remove(side)
        if not back_stopper_present and (back_piece in self.sides_outter):
            stopper = self.remove_whole_side(back_piece)
            if stopper:
                stoppers_present.add(stopper)
        if not fore_stopper_present and (fore_piece in self.sides_outter):
            stopper = self.remove_whole_side(fore_piece)
            if stopper:
                stoppers_present.add(stopper)

        return stoppers_present.pop() if (len(stoppers_present) > 0) else None

    def sides(self):
        self.sides_outter = set()
        for plot in self.plots:
            for side in plot.sides_outter:
                self.sides_outter.add(side)

        next_side = None
        side_count = 0
        while len(self.sides_outter) > 0:
            if not next_side:
                next_side = list(self.sides_outter)[0]
            side_count += 1
            next_side = self.remove_whole_side(next_side)

        # print(side_count)
        return side_count

class Garden:
    def __init__(self):
        self.area = []
        self.width = 0
        self.height = 0
        self.regions = []

    def add_line(self, line):
        row = []
        self.width = len(line)
        r = self.height
        for c, chr in enumerate(list(line)):
            row.append(Plot(chr, Coordinate(r, c)))
        self.area.append(row)
        self.height += 1

    def print(self):
        for row in self.area:
            row_text = ""
            for plot in row:
                row_text += plot.type
            print(row_text)

    def coordinate_is_valid(self, coordinate):
        return (0 <= coordinate.r < self.height) and (0 <= coordinate.c < self.width)

    def categorize_neighbors(self, plot):
        all_sides = plot.get_side_coordinates()
        for neighbor_coordinate in plot.get_neighbor_coordinates():
            if self.coordinate_is_valid(neighbor_coordinate):
                neighbor = self.area[neighbor_coordinate.r][neighbor_coordinate.c]
                if neighbor.type == plot.type:
                    plot.neighbors_same.add(neighbor)
                    all_sides.remove(plot.side_between(neighbor))
                else:
                    plot.neighbors_different.add(neighbor)
        plot.sides_outter = set(all_sides)

    def categorize_all_neighbors(self):
        for row in self.area:
            for plot in row:
                self.categorize_neighbors(plot)

    def find_entire_region(self, plot, region):
        if plot.region or (plot.type != region.type):
            return

        # This plot should be in the region, so associate them
        plot.region = region
        region.plots.add(plot)
        for neighbor in plot.neighbors_same:
            self.find_entire_region(neighbor, region)

    def find_all_regions(self):
        for row in self.area:
            for plot in row:
                if not plot.region:
                    new_region = Region(plot.type)
                    self.regions.append(new_region)
                    self.find_entire_region(plot, new_region)

    def find_price(self):
        price = 0
        for region in self.regions:
            price += region.area() * region.perimeter()
        return price

    def find_new_price(self):
        price = 0
        for region in self.regions:
            price += region.area() * region.sides()
        return price

def get_garden():
    garden = Garden()
    for line in next_line(input_file):
        garden.add_line(line.strip())
    return garden

def do_part_1():
    garden = get_garden()
    garden.categorize_all_neighbors()
    garden.find_all_regions()
    price = garden.find_price()
    print(f"{price} for {len(garden.regions)} regions")

def do_part_2():
    garden = get_garden()
    garden.categorize_all_neighbors()
    garden.find_all_regions()
    price = garden.find_new_price()
    print(f"{price} for {len(garden.regions)} regions")

do_part_1()
do_part_2()
