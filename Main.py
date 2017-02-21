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
    def toppingsInCut(self, co1, co2):
        tomatos = 0
        mushrooms = 0
        start_r = min(co1[0], co2[0])
        start_c = min(co1[1], co2[1])
        for r in range(abs(co1[0] - co2[0])):
            curr_r = start_r + r
            for c in range(abs(co1[1] - co2[1])):
                curr_c = start_c + c
                if self.grid[curr_r][curr_c] == "T":
                    tomatos += 1
                elif self.grid[curr_r][curr_c] == "M":
                    mushrooms += 1

        return (tomatos, mushrooms)

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

def bigCuts(pizzas):
    #We do only cuts according to the size H
    cuts = []


    return cuts