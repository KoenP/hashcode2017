from ClassFile import CacheServer
from alg2 import timeSaved, cacheToEndpointAssocList, endpointVideoToReqDict
import operator

def exec_alg(data):
    print("Running algorithm 1 on {}...".format(data["filename"]))
    requests = data['Rqs']
    temp_requests = []
    video_sizes = data['S']

    total_video_requests = [0] * data['V']
    for r in requests:
        # r[0] vid id
        # r[2] vid requests
        total_video_requests[r[0]] += r[2]
    #cte = cacheToEndpointAssocList(data)
    #rqd = endpointVideoToReqDict(data)

    for r in requests:
        # r[2] vid requests
        temp_requests.append((r[0], r[1], r[2], total_video_requests[r[0]] * r[2]/video_sizes[r[1]]))

    requests = temp_requests
    #Sort on weight
    requests.sort(key=operator.itemgetter(3), reverse=True)

    # id, server
    cache_servers = []
    latencies = {}
    endpoint_cache_servers = {}

    for k,v in data['Lc'].items():

        # k[1] is the cache id
        if k[1] not in latencies:
            latencies[k[1]] = {}

        if k[0] not in endpoint_cache_servers:
            endpoint_cache_servers[k[0]] = []

        # k[1] cache server
        # k[0] endpoint id
        # v is latency
        latencies[k[1]][k[0]] = v

        endpoint_cache_servers[k[0]].append(k[1])

    for c in range(data['C']):
        # Latencies is a list of tupples
        # first entry endpoint id
        # second entry is latency
        cache_servers.append(CacheServer(c,data['X'],latencies[c]))

    ld = data['Ld']

    for r in requests:
        current_endpoint = r[1]
        if current_endpoint in endpoint_cache_servers:
            current_cache_servers = endpoint_cache_servers[current_endpoint]

            servers = []
            for c in current_cache_servers:
                servers.append(cache_servers[c])

            # Check if the video is in one of the cache servers of the endpoint
            in_servers = False
            for s in servers:
                if r[0] in s.cached_videos:
                    in_servers = True
                    break

            #servers.sort(key=lambda x: timeSaved(data,cte, rqd, x.id, r[0]) * r[2] / video_sizes[r[0]], reverse=True)

            if not in_servers:
                servers.sort(
                    key=lambda x: (ld[current_endpoint] - x.latencies[current_endpoint]) * r[2] / video_sizes[r[0]],
                    reverse=True)

                for s in servers:
                    if s.addVideo(r[0], video_sizes[r[0]]):
                        break

    return cache_servers
