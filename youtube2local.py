import importlib
import json
import sys

import youtube_dl

import config
from helpers import title

backend = importlib.import_module("backends.%s" % config.config["backend"])


class MyLogger():
    """
    Custom logger for YoutubeDL.
    """
    def debug(self, msg):
        if msg.startswith("[download]"):
            print(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


# YoutubeDL options
YDL_OPTS = {
    'logger': MyLogger(),
    'ignoreerrors': True,
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def match(youtube_url):
    """
    Match videos from a Youtube URL with a local music collection.

    Params:
        - youtube_url is the Youtube URL to fetch and match.

    Returns:
        A list of dict for every Youtube video in the Youtube link (single
        video or playlist). Each dict contains the Youtube title, the video
        webpage URL, the video download URL, and an eventual match
        (None if none found).
    """
    # Fetch infos for Youtube link
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        result = ydl.extract_info(youtube_url, download=False)

    # Single video
    if "entries" not in result:
        result = {"entries": [result]}

    # Parse every song
    songs = []
    for entry in result["entries"]:
        # Try to fetch metadata from the title
        metadata = title.split(entry["title"])
        if metadata is not None:
            # Try to find a match
            song_match = backend.check_metadata(metadata, config.config),
            if match is not None:
                songs.append({
                    "match": song_match,
                    "yt_title": entry["title"],
                    "url": entry["webpage_url"]
                })
                # Go on with next song
                continue
        # Add the song to the list, with its eventual match
        songs.append({
            "match": backend.check_title(title.clean(entry["title"]),
                                         config.config),
            "yt_title": entry["title"],
            "url": entry["webpage_url"]
        })
    return songs


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: %s YOUTUBE_URL" % sys.argv[0])

    print(json.dumps(match(sys.argv[1]),
                     sort_keys=True, indent=4, separators=(',', ': ')))
