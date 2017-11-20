from __future__ import unicode_literals

from apiclient.discovery import build
import httplib2
import youtube_dl

import os
import sys


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

    def download(self, playlists):
        for playlist in playlists:
            ydl_opts = {
                'ignoreerrors': True,
                'download_archive': '{} archive.txt'.format(playlist["title"]),
                'outtmpl': '%(playlist)s/%(title)s-%(id)s.%(ext)s'
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(['https://www.youtube.com/playlist?list={}'
                              .format(playlist["id"])])

    def go(self):
        self.download(self.playlists())


if __name__ == "__main__":
    user_id = sys.argv[1]
    Archiver(user_id).go()
