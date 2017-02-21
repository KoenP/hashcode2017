class Pizza:

    def __init__(self, row, column, L, H, layout):
        self.row = row
        self.column = column
        self.L = L
        self.H = H
        self.grid = layout

# Returns a pizza
def parse(filename):
    pass

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




