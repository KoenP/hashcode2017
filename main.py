import os
import sys

import alg1
import alg2
import alg3
import alg4

# Struct for wrapping all useful information in regards to the problem inputs
class ProblemData:
    def __init__(self, filename):
        self.filename = filename

# Reads file with name filename and outputs ProblemData object
def parse(filename):
    with open(filename, mode="r") as ifs:
        lines = ifs.readlines()

        # TODO: Do stuff with lines and add in ProblemData object

        # Return problem data
        return ProblemData(filename[6:])

# Output the solution
def output(filename, solution):
    # Cut off 'input/'
    with open('output_{}.txt'.format(filename[6:-3]), mode="w") as ofs:
        print("Outputting solution for {}...".format(filename[6:]))

        # TODO: do useful writes
        ofs.write(filename)


# Usage: python3 <algorithm> <inputfile OR 'all'>
if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Parse input file(s)
        inputs = ["input/" + sys.argv[2]]
        if sys.argv[2] == "all":
            inputs = ["input/{}".format(f) for f in os.listdir('input') if f.endswith(".in")]

        problem_datas = list(map(parse, inputs))

        solutions = list(map(globals()[sys.argv[1]].exec_alg, problem_datas))

        _ = list(map(output, inputs, solutions))

    elif len(sys.argv) == 2:
        print("ERROR: algorithm and input file required.")

    # print(globals())
