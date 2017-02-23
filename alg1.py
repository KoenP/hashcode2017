from ClassFile import CacheServer
from alg2 import timeSaved, cacheToEndpointAssocList, endpointVideoToReqDict
import operator

# Get the avg latency for one endpoint
def getAvgLatencyEndpoint(ld, cache_servers):
    avg_latencies = {}
    for c in cache_servers:
        for l,v in c.latencies.items():
            if l not in avg_latencies:
                # first item is how many latencies we got
                # total amount of latency
                avg_latencies[l] = [0, 0]

            avg_latencies[l][0] += 1
            avg_latencies[l][1] += ld[l] - v

    latencies = {}
    for k,v in avg_latencies.items():
        latencies[k] = avg_latencies[k][1] / avg_latencies[k][0]

    return latencies


def getAvgWinCache(ld, endpoint_cache_servers, requests, cache_servers):
    win = {}
    for r in requests:
        current_endpoint = r[1]

        if current_endpoint in endpoint_cache_servers:
            current_cache_servers = endpoint_cache_servers[current_endpoint]

            for s in current_cache_servers:
                c = cache_servers[s]
                cur_latency = c.latencies[r[1]]
                w = ld[r[1]] - cur_latency
                if c.id not in win:
                    win[c.id] = [0, 0]

                win[c.id][0] += 1
                win[c.id][1] += w * r[2]

    avg_win = {}
    for k,v in win.items():
        avg_win[k] = win[k][1] / win[k][0]

    return avg_win


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
    #avg_latencies = getAvgLatencyEndpoint(ld, cache_servers)
    avg_win = getAvgWinCache(ld, endpoint_cache_servers, requests, cache_servers)
    for r in requests:
        current_endpoint = r[1]
        if current_endpoint in endpoint_cache_servers:
            current_cache_servers = endpoint_cache_servers[current_endpoint]

            servers = []
            for c in current_cache_servers:
                servers.append(cache_servers[c])

            # Check if the video is in one of the cache servers of the endpoint
            in_servers = False
            # lowest_latency = float('inf')
            # for s in servers:
            #     l = s.latencies[current_endpoint]
            #     if l < lowest_latency:
            #         lowest_latency = l

            for s in servers:
                if r[0] in s.cached_videos and (ld[current_endpoint] - s.latencies[current_endpoint]) * r[2] >= avg_win[s.id]:
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
