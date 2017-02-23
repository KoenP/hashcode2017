from recipes import *

def exec_alg(params):
    print("Running algorithm 2 on {}...".format(params["filename"]))
    cte = cacheToEndpointAssocList(params)
    rqd = endpointVideoToReqDict(params)
    return solve(params, cte, rqd)

def solve(params, cte, rqd):
    # TODO sorteer caches op latency
    allocation = [[] for _ in range(params['C'])]
    for cacheId in sorted(range(params['C']), key=lambda cId: len(cte[cId])):
        ad = allocationsIndexedByVid(params, allocation)
        def ts(vid):
            tsaved = timeSaved2(params, cte, rqd, ad, cacheId, vid)
            size = params['S'][vid]
            return tsaved
        sortedVids = range(params['V'])
        sortedVids = sorted(range(params['V']), key=ts, reverse=True)
        cacheCapacity = params['X']
        curSize = 0
        while sortedVids:
            v = sortedVids[0]
            sortedVids = sortedVids[1:]
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

def allocationsIndexedByVid(params, allocations):
    # TODO untested
    d = [[] for _ in range(params['V'])]
    for cacheId, vidList in enumerate(allocations):
        for v in vidList:
            d[v] += [cacheId]
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

# TODO
def timeSaved2(params, cte, rqd, allocationsIndexedByVid, cacheId, videoId):
    result = 0
    endpoints = cte[cacheId]
    cachesAllocatedTo = allocationsIndexedByVid[videoId]
    for e in endpoints:
        reqs = rqd.get((e, videoId))
        if reqs is not None:
            latencyDict = params['Lc']
            ld = params['Ld'][e]
            lc = latencyDict[(e,cacheId)]
            if cachesAllocatedTo:
                lc *= 3.5
            minCacheLatency = \
                min(filter(lambda x: x is not None, \
                           chain([ld], map(lambda c: latencyDict.get((e,c)), \
                                           cachesAllocatedTo))))
            result += max(0, minCacheLatency - lc) * reqs
    return result
