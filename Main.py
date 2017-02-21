import math
import sys

class Pizza:

    def __init__(self, row, column, L, H, layout):
        self.row = row
        self.column = column
        self.L = L
        self.H = H
        self.grid = layout

    # co1 is coordinate 1
    # co2 is coordinate 2
    # returns the amount of tomatos and mushrooms in a cut in the form of a tupple
    def toppingsInSlice(self, co1, co2):
        tomatos = 0
        mushrooms = 0
        start_r = min(co1[0], co2[0])
        start_c = min(co1[1], co2[1])
        for r in range(abs(co1[0] - co2[0]) + 1):
            curr_r = start_r + r
            for c in range(abs(co1[1] - co2[1]) + 1):
                curr_c = start_c + c
                if curr_c >= self.column or curr_r >= self.row:
                    continue
                if self.grid[curr_r][curr_c] == "T":
                    tomatos += 1
                elif self.grid[curr_r][curr_c] == "M":
                    mushrooms += 1

        return (tomatos, mushrooms)

    # coord the starting point for our slice
    # all our slices
    # return the slice our coord is in
    # none if there is no slice
    def coordInSlices(self, coord, slices):
        for s in slices:
            co1 = s[0]
            co2 = s[1]

            if coord[0] >= min(co1[0], co2[0]) and coord[0] <= max(co1[0], co2[0]) \
                    and coord[1] >= min(co1[1], co2[1]) and coord[1] <= max(co1[1], co2[1]):
                return s
        return None

    def validSlice(self, slice):
        co1 = slice[0]
        co2 = slice[1]

        if co1[0] <= self.row and co2[0] <= self.row and co1[1] <= self.column and co2[1] <= self.column:
            return True

        return False

# Returns a pizza
def parse(filename):
    f = open(filename)
    lines = f.readlines()

    [rows, columns, L, H] \
        = map(int, lines[0].split())

    layout = [[] for _ in range(rows)]
    for (i, line) in enumerate(lines[1:]):
        layout[i] = list(map(lambda x:x, line[:-1]))

    return Pizza(rows, columns, L, H, layout)

# format slices: [((r_11,c_11), (r_12,c_12)), ((r_21,c_21), (r_22,c_22)), ...]
# returns the points for the slices
def evaluateSlices(slices):
    points = 0
    for s in slices:
        points += abs(s[1][0] - s[0][0] + 1) * abs(s[1][1] - s[0][1] + 1)
    return points

# various algs

# Encodes slices to output format (same format as above)
def slicesToOutput(slices):
    f = open('output.txt', 'w')
    f.write("{}\n".format(len(slices)))

    for s in slices:
        f.write("{} {} {} {}\n".format(s[0][0], s[0][1], s[1][0], s[1][1]))
    f.close()

def allSlicesForPosWithSize(pos, s):
    slices = []
    horizontal = (pos, (pos[0],pos[1] + s))
    vertical = (pos, (pos[0]+s, pos[1]))
    slices.append(horizontal)
    slices.append(vertical)
    start_r = pos[0]
    start_c = pos[1]

    for i in range(1, math.floor(math.sqrt(s))):
        # horizontal rectangle
        c = math.floor(s/(i+1)) - 1
        slices.append((pos, (start_r + i, start_c + c)))

        # same length for vertical
        r = c
        slices.append((pos, (start_r + r, start_c + i)))

    return slices


def growSlice(pizza, currentSlices):
    # We first need to find a coord that is outside the currentSlices
    startCo = None
    triedPos = []
    r = 0
    c = 0
    while r < pizza.row:
        while c < pizza.column:
            slice = pizza.coordInSlices((r, c), currentSlices)
            if slice is None and (r,c) not in triedPos:
                startCo = (r,c)
                triedPos.append(startCo)
                break
            elif slice is not None:
                co1 = slice[0]
                co2 = slice[1]
                c = max(co1[1], co2[1]) + 1
            else:
                c += 1

            print(r,c)

        if startCo is not None:
            break

        r += 1
    if startCo is None:
        return None

    #We found a starting point, now grow our slice!
    #What we really want is the biggest slide we can create
    slices = allSlicesForPosWithSize(startCo, pizza.H)

    sum = 0
    slice = None
    for s in slices:
        # First check if the slice is in the board
        if not pizza.validSlice(s):
            continue

        co1 = s[0]
        co2 = s[1]

        (t,m) = pizza.toppingsInSlice(co1, co2)

        #Check if we have enough toppings
        if not(t >= pizza.L and m >= pizza.L):
            continue
        if t+m > sum:
            sum = t+m
            slice = s

    return slice

def bigSlices(pizza):
    #We do only cuts according to the size H
    cuts = []
    while True:
        s = growSlice(pizza,cuts)
        if s is None:
            break
        cuts.append(s)
        print(cuts)
    return cuts

# format slices: [((r_11,c_11), (r_12,c_12)), ((r_21,c_21), (r_22,c_22)), ...]
def topDownSlicing(pizza):
    for i in range(pizza.columns):
        if sensible(pizza, i):
            pass

def sensible(pizza, index):
    pass


def main(argv):
    p = parse(argv[1])
    slices = bigSlices(p)
    slicesToOutput(slices)
    print(evaluateSlices(slices))

if __name__ == "__main__":
   main(sys.argv)