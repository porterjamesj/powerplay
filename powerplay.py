from apiclient.discovery import build
import httplib2

import os


class Archiver(object):

    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.client = build(
            "youtube",
            "v3",
            http=httplib2.Http(),
            developerKey=os.getenv("YOUTUBE_API_KEY")
        )

    def playlists(self):
        req = self.client.playlists().list(
            part="snippet",
            channelId=self.channel_id,
        )
        ret = []
        while req is not None:
            resp = req.execute()
            ret.extend({"id": p["id"], "title": p["snippet"]["title"]}
                       for p in resp["items"])
            req = self.client.playlists().list_next(req, resp)

        # Liked videos doesn't show up in the above, so we have to get
        # it out of the channel info

        resp = self.client.channels().list(
            part="contentDetails", id=self.channel_id
        ).execute()
        assert len(resp["items"]) == 1
        channel = resp["items"][0]

        liked_videos_id = channel["contentDetails"]["relatedPlaylists"]["likes"]
        ret.append({"id": liked_videos_id, "title": "Liked videos"})
        return ret

    def download(playlist)




if __name__ == "__main__":
    porterjamesj = "UCoDRCiVwKsjhqT2nXHmE3zg"
    a = Archiver(porterjamesj)
    import pprint
    pprint.pprint(a.gather())
