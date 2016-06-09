"""
Helper to clean Youtube titles, removing usual junk.
"""
import re


def find_separator(str):
    """
    Find a common separators used in Youtube titles to separate artist and
    track name.
    """
    separators = [' -- ', ' - ', ' – ', ' — ', '///', '►']
    if len(str) == 0:
        return None

    for sep in separators:
        index = str.find(sep)
        if index > -1:
            return {
                "index": index,
                "length": len(sep)
            }

    return None


def split(yt_title):
    """
    Split a title according to found separator.
    """
    # Find separator
    separator = find_separator(yt_title)
    if separator is None or len(yt_title) == 0:
        return {
            "artist": None,
            "title": None
        }

    # Split artist and title
    artist = yt_title[0:separator["index"]]
    title = yt_title[separator["index"] + separator["length"]:]

    # Do some cleanup
    artist = clean(artist)
    title = clean(title)

    return {
        "artist": artist,
        "title": title
    }


def clean(title):
    """
    Remove usual junk from a Youtube title.
    """
    title = re.sub(r"/^\s+|\s+$/g", '', title)
    # **NEW**
    title = re.sub(r"/\s*\*+\s?\S+\s?\*+$/", '', title)
    # [whatever]
    title = re.sub(r"/\s*\[[^\]]+\]$/", '', title)
    # (whatever version)
    title = re.sub(r"/\s*\([^\)]*version\)$/i", '', title)
    # video extensions
    title = re.sub(r"/\s*\.(avi|wmv|mpg|mpeg|flv)$/i", '', title)
    # (LYRIC VIDEO)
    title = re.sub(r"/\s*(LYRIC VIDEO\s*)?(lyric video\s*)/i", '', title)
    # (Official title Stream)
    title = re.sub(r"/\s*(Official title Stream*)/i", '', title)
    # (official)? (music)? video
    title = re.sub(r"/\s*(of+icial\s*)?(music\s*)?video/i", '', title)
    # (official)? (music)? audio
    title = re.sub(r"/\s*(of+icial\s*)?(music\s*)?audio/i", '', title)
    # (ALBUM title)
    title = re.sub(r"/\s*(ALBUM title\s*)?(album title\s*)/i", '', title)
    # (Cover Art)
    title = re.sub(r"/\s*(COVER ART\s*)?(Cover Art\s*)/i", '', title)
    # (official)
    title = re.sub(r"/\s*\(\s*of+icial\s*\)/i", '', title)
    # (1999)
    title = re.sub(r"/\s*\(\s*[0-9]{4}\s*\)/i", '', title)
    # HD (HQ)
    title = re.sub(r"/\s+\(\s*(HD|HQ)\s*\)$/", '', title)
    # HD (HQ)
    title = re.sub(r"/\s+(HD|HQ)\s*$/", '', title)
    # video clip
    title = re.sub(r"/\s*video\s*clip/i", '', title)
    # Full Album
    title = re.sub(r"/\s*full\s*album/i", '', title)
    # live
    title = re.sub(r"/\s+\(?live\)?$/i", '', title)
    # Leftovers after e.g. (official video)
    title = re.sub(r"/\(+\s*\)+/", '', title)
    # Artist - The new "title title" featuring someone
    title = re.sub(r"/^(|.*\s)\"(.*)\"(\s.*|)$/", '\2', title)
    # 'title title'
    title = re.sub(r"/^(|.*\s)'(.*)'(\s.*|)$/", '\2', title)
    # trim white chars and dash
    title.lstrip(" \t\n\r-")
    title.rstrip(" \t\n\r-")

    return title
