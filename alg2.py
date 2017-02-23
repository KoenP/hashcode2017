from recipes import *

def exec_alg(data):
    print("Running algorithm 2 on {}...".format(data["filename"]))

    return []

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

        # Requests
        def parseReqLine(line):
            [v, e, r] = map(int, line.split())
            return (v, e, r)
        dictionary['Rqs'] = list(map(parseReqLine, lines[line:]))

        # Return problem data
        return dictionary

params = parse('input/example.in')
def cacheToEndpointAssocList(params):
    al = [[] for _ in range(params['C'])]
    for (endpoint, cacheId) in params['Lc']:
        al[cacheId] += [endpoint]
    return al
def endpointVideoToReqDict(params):
    d = {}
    for (v, e, r) in params['Rqs']:
        d[(e,v)] = r
    return d
cte = cacheToEndpointAssocList(params)
rqd = endpointVideoToReqDict(params)

def timeSaved(params, cacheId, videoId):
    result = 0
    endpoints = cte[cacheId]
    for e in endpoints:
        reqs = rqd.get((e, videoId))
        if reqs is not None:
            ld = params['Ld'][e]
            lc = params['Lc'][(e,cacheId)]
            result += (ld - lc) * reqs
    return result
