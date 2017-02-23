from recipes import *

def exec_alg(params):
    print("Running algorithm 2 on {}...".format(data["filename"]))
    cte = cacheToEndpointAssocList(params)
    rqd = endpointVideoToReqDict(params)
    solve(params, cte, rqd)
    return []

#def solve(params, cte, rqd):
#    allocation = [[] for _ in range(params['C'])]
#    for cacheId in range(params['C']):
#        sorted(range(params['V']), 

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

def timeSaved(params, cte, rqd, cacheId, videoId):
    result = 0
    endpoints = cte[cacheId]
    for e in endpoints:
        reqs = rqd.get((e, videoId))
        if reqs is not None:
            ld = params['Ld'][e]
            lc = params['Lc'][(e,cacheId)]
            result += (ld - lc) * reqs
    return result

