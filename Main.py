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
                if self.grid[curr_r][curr_c] == "T":
                    tomatos += 1
                elif self.grid[curr_r][curr_c] == "M":
                    mushrooms += 1

        return (tomatos, mushrooms)

    def coordInSlices(self, coord, slices):
        for s in slices:
            co1 = s[0]
            co2 = s[1]
            if coord[0] >= min(co1[0], co2[0]) and coord[0] <= max(co1[0], co2[0]) \
                and coord[1] >= min(co1[1], co2[1]) and coord[1] <= max(co1[1], co2[1]):
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
        points += abs(s[1][0] - s[0][0]) * abs(s[1][1] - s[0][1])
    return points

# various algs

# Encodes slices to output format (same format as above)
def slicesToOutput(slices):
    f = open('output.txt', 'w')
    f.write(len(slices))
    for s in slices:
        f.write("{} {} {} {}\n".format(s[0][0], s[0][1], s[1][0], s[1][1]))
    f.close()

def growSlice(pizza, currentSlices):
    pass

def bigCuts(pizza):
    #We do only cuts according to the size H
    cuts = []
    return cuts

def isGoodSlice(pizza):
    return pizza.row * pizza.column <= pizza.H

# format slices: [((r_11,c_11), (r_12,c_12)), ((r_21,c_21), (r_22,c_22)), ...]
def topDownSlicing(pizza):

    if isGoodSlice(pizza):
        return [((0,0), (pizza.row-1, pizza.column-1))]

    transpose = pizza.row > pizza.column

    if transpose:
        pizza.grid = transpose_grid(pizza.grid)

    sensibles = [(i, cost(pizza, i)) for i in range(pizza.column - 1) if sensible(pizza, i)]
    min_col = min(sensibles, key=lambda t: t[1])

    layout1 = [line[:min_col[0]] for line in pizza.grid]
    layout2 = [line[min_col[0]+1:] for line in pizza.grid]

    new_pizza1 = Pizza(pizza.row, min_col[0], pizza.L, pizza.H, layout1)
    new_pizza2 = Pizza(pizza.row, pizza.column - min_col[0], pizza.L, pizza.H, layout2)

    result1 = topDownSlicing(new_pizza1)
    result2 = topDownSlicing(new_pizza2)

    detranspose = lambda slice: ((slice[0][1], slice[0][0]), (slice[1][1], slice[1][0]))

    if transpose:
        result1 = list(map(detranspose, result1))
        result2 = list(map(detranspose, result2))

    return result1 + result2

def transpose_grid(grid):
    return [[row[i] for row in grid] for i in range(len(grid[0]))]


# TODO: performance is garbage
def sensible(pizza, index):
    tomatos1, mushrooms1 = pizza.toppingsInSlice((0, 0), (pizza.row-1, index))
    tomatos2, mushrooms2 = pizza.toppingsInSlice((0, index+1), (pizza.row-1, pizza.column-1))
    return all(map(lambda i: i >= pizza.L, [tomatos1, mushrooms1, tomatos2, mushrooms2]))

def cost(pizza, index):
    T, M = pizza.toppingsInSlice((0,0), (pizza.row-1, pizza.column-1))
    ratio = T/M
    tomatos1, mushrooms1 = pizza.toppingsInSlice((0, 0), (pizza.row-1, index))
    tomatos2, mushrooms2 = pizza.toppingsInSlice((0, index+1), (pizza.row-1, pizza.column-1))
    # print(T, M, ratio, tomatos1/mushrooms1, tomatos2/mushrooms2)
    return abs(ratio - tomatos1/mushrooms1) + abs(ratio - tomatos2/mushrooms2)
