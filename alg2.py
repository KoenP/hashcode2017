from recipes import *

def exec_alg(params):
    print("Running algorithm 2 on {}...".format(params["filename"]))
    cte = cacheToEndpointAssocList(params)
    rqd = endpointVideoToReqDict(params)
    return solve(params, cte, rqd)

def solve(params, cte, rqd):
    allocation = [[] for _ in range(params['C'])]
    for cacheId in range(params['C']):
        def ts(vid):
            tsaved = timeSaved(params, cte, rqd, cacheId, vid)
            size = params['S'][vid]
            return tsaved/size
        sortedVids = sorted(range(params['V']), key=ts, reverse=True)
        cacheCapacity = params['X']
        curSize = 0
        for v in sortedVids:
            vSize = params['S'][v]
            newSize = curSize + vSize
            if newSize <= cacheCapacity:
                allocation[cacheId] += [v]
                curSize = newSize
    return allocation


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

