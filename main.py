import os
import sys

import alg1
import alg2
import alg3
import alg4

# Reads file with name filename and outputs dictionary
def parse(filename):
    with open(filename, mode="r") as ifs:
        lines = ifs.readlines()
        dictionary = {"filename": filename[6:]}

        # Line 1 (VERCX)
        [V, E, R, C, X] = map(int, lines[0].split())
        dictionary['V'] = V
        dictionary['E'] = E
        dictionary['R'] = R
        dictionary['C'] = C
        dictionary['X'] = X

        # Line 2 (video sizes)
        dictionary['S']= list(map(int, lines[1].split()))

        # Latencies
        line = 2
        endpoint = 0
        dictionary['Ld'] = [0 for _ in range(E)]
        dictionary['Lc'] = {}
        while endpoint < E:
            [L, K] = map(int, lines[line].split())
            dictionary['Ld'][endpoint] = L
            for j in range(K):
                [cacheId, latency] = map(int, lines[line+j+1].split())
                dictionary['Lc'][(endpoint,cacheId)] = latency
            endpoint += 1
            line += K+1

        


        # Return problem data
        return dictionary

# Output the solution
def output(filename, solution):
    # Cut off 'input/'
    with open('output_{}.txt'.format(filename[6:-3]), mode="w") as ofs:
        print("Outputting solution for {}...".format(filename[6:]))
        used_servers = 0
        output = ""
        for s in solution:
            if s.current_cap > 0:
                used_servers += 1
                output += s.outputServer() + "\n"

        ofs.write("{}\n {}".format(used_servers, output))


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
