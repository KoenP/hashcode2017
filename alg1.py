from ClassFile import CacheServer
import operator

def exec_alg(data):

    print(data)
    print("Running algorithm 1 on {}...".format(data["filename"]))
    requests = data['Rqs']
    temp_requests = []
    video_sizes = data['S']

    for r in requests:
        temp_requests.append((r[0], r[1], r[2], r[2]/video_sizes[r[1]]))

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
            latencies[k[1]] = []

        if k[0] not in endpoint_cache_servers:
            endpoint_cache_servers[k[0]] = []

        latencies[k[1]].append((k[0],v))
        endpoint_cache_servers[k[0]].append(k[1])

    for c in range(data['C']):
        cache_servers.append(CacheServer(c,data['X'],latencies[c]))

    for r in requests:
        current_endpoint = r[1]
        if current_endpoint in endpoint_cache_servers:
            current_cache_servers = endpoint_cache_servers[current_endpoint]

            servers = []
            for c in current_cache_servers:
                servers.append(cache_servers[c])

            servers.sort(key=lambda x: x.latencies[current_endpoint], reverse=True)

            # random adding
            for s in servers:
                if s.addVideo(r[0], video_sizes[r[0]]):
                    break

    return cache_servers
