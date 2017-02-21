class Pizza:

    def __init__(self, row, column, L, H, layout):
        self.row = row
        self.column = column
        self.L = L
        self.H = H
        self.grid = layout

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
def evaluateSlices(pizza, slices):
    pass

# various algs

# Encodes slices to output format (same format as above)
def slicesToOutput(slices):
    pass
