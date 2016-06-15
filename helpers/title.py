"""
Helper to clean Youtube titles, removing usual junk.

Adapted from
https://github.com/david-sabata/web-scrobbler/blob/master/connectors/v2/youtube.js
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
        return None

    # Split artist and title
    artist = yt_title[0:separator["index"]]
    title = yt_title[separator["index"] + separator["length"]:]

    # Do some cleanup
    artist = clean(artist)
    title = clean(title)

    return {
        "artist": artist,
        "title": title,
        "album": None
    }


def clean(title):
    """
    Remove usual junk from a Youtube title.
    """
    title = re.sub(r"^\s+|\s+$g", '', title)
    # **NEW**
    title = re.sub(r"\s*\*+\s?\S+\s?\*+$", '', title)
    # [whatever]
    title = re.sub(r"\[[^\]]+\]$", '', title)
    # (whatever version)
    title = re.sub(r"(?i)\s*\([^\)]*version\)$", '', title)
    # video extensions
    title = re.sub(r"(?i)\s*\.(avi|wmv|mpg|mpeg|flv)$", '', title)
    # (LYRIC VIDEO)
    title = re.sub(r"(?i)(LYRIC VIDEO\s*)?(lyric video\s*)", '', title)
    # (Official title Stream)
    title = re.sub(r"(?i)(Official title Stream*)", '', title)
    # (official)? (music)? video
    title = re.sub(r"(?i)(of+icial\s*)?(music\s*)?video", '', title)
    # (official)? (music)? audio
    title = re.sub(r"(?i)\s*(of+icial\s*)?(music\s*)?audio", '', title)
    # (ALBUM title)
    title = re.sub(r"(?i)\s*(ALBUM title\s*)?(album title\s*)", '', title)
    # (Cover Art)
    title = re.sub(r"(?i)\s*(COVER ART\s*)?(Cover Art\s*)", '', title)
    # (official)
    title = re.sub(r"(?i)\s*\(\s*of+icial\s*\)", '', title)
    # (1999)
    title = re.sub(r"(?i)\s*\(\s*[0-9]{4}\s*\)", '', title)
    # HD (HQ)
    title = re.sub(r"\s+\(\s*(HD|HQ)\s*\)$", '', title)
    # HD (HQ)
    title = re.sub(r"\s+(HD|HQ)\s*$", '', title)
    # video clip
    title = re.sub(r"(?i)\s*video\s*clip", '', title)
    # Full Album
    title = re.sub(r"(?i)\s*full\s*album", '', title)
    # live
    title = re.sub(r"(?i)\s+\(?live\)?$", '', title)
    # Leftovers after e.g. (official video)
    title = re.sub(r"\(+\s*\)+", '', title)
    # Remove featurings
    title = re.sub(r"\(feat\. .*?\)", '', title)
    # 'title title'
    title = re.sub(r"^(|.*\s)'(.*)'(\s.*|)$", '\2', title)
    # trim white chars, dash and quotes
    title = title.strip()
    title = title.strip("-\"'")

    return title
