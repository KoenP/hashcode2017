class CacheServer:

    def __init__(self,s_id, max_cap, latency):
        self.id = s_id
        self.max_cap = max_cap
        self.current_cap = 0
        self.latency = latency
        self.cached_videos = []

    # returns true if we can add the video to the cache
    # returns false otherwise
    def addVideo(self, video_id, vid_size):
        if self.current_cap + vid_size <= self.max_cap:
            self.cached_videos.append(video_id)
            self.current_cap += vid_size
            return True
        return False

    def outputServer(self):
        output = str(self.id)
        for v in self.cached_videos:
            output += " {}".format(v)
        return output

