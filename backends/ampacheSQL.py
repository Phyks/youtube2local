"""
Checks if a song exist against Ampache SQL database directly.
"""
import MySQLdb
import MySQLdb.cursors

def check_title(str, config):
    """
    Check if a song is in the Ampache catalog.

    Params:
        - str is a string ot match against song names, artists, albums etc
        - config is a configuration dictionary.

    Returns:
        A dict containing the found infos about the song or None.
    """
    db = MySQLdb.connect(user=config["db_user"], host=config["db_host"],
                         passwd=config["db_password"],
                         db=config["db_name"],
                         cursorclass=MySQLdb.cursors.DictCursor)

    c = db.cursor()
    c.execute("""SELECT
              song.id AS id,
              artist.name AS artist,
              album.name AS album,
              song.title AS title,
              song.file AS file,
              MATCH(artist.name, album.name, song.title)
              AGAINST(%s IN BOOLEAN MODE) AS score
              FROM song
              LEFT JOIN artist ON song.artist = artist.id
              LEFT JOIN album ON song.album = album.id
              WHERE MATCH(artist.name, album.name, song.title)
              AGAINST(%s IN BOOLEAN MODE)
              ORDER BY score DESC LIMIT 1""", (str, str,))
    return c.fetchone()


def check_metadata(metadata, config):
    """
    Check if a song is in the Ampache catalog.

    Params:
        - metadata, an artist/title/album dictionary. Album key is optional.
        - config is a configuration dictionary.

    Returns:
        A dict containing the found infos about the song or None.
    """
    db = MySQLdb.connect(user=config["db_user"], host=config["db_host"],
                         passwd=config["db_password"],
                         db=config["db_name"],
                         cursorclass=MySQLdb.cursors.DictCursor)

    c = db.cursor()

    sql = """SELECT
             song.id AS id,
             artist.name AS artist,
             album.name AS album,
             song.title AS title,
             song.file AS file,
             ("""
    args = tuple([])
    if len(metadata["artist"]) > 3:
        sql += "MATCH(artist.name) AGAINST(%s IN BOOLEAN MODE)"
        args += (metadata["artist"],)
    else:
        sql += "0"

    if len(metadata["title"]) > 3:
        sql += " + MATCH(song.title) AGAINST(%s IN BOOLEAN MODE)"
        args += (metadata["title"],)

    if "album" in metadata and metadata["album"] is not None and len(metadata["album"]) > 3:
        sql += " + MATCH(album.name) AGAINST(%s IN BOOLEAN MODE)"
        args += (metadata["album"],)

    sql += """) AS score
              FROM song
              LEFT JOIN artist ON song.artist = artist.id
              LEFT JOIN album ON song.album = album.id"""

    if not len(metadata["artist"]) > 3:
        sql += " WHERE artist.name LIKE %s"
        args += ("%%%s%%" % (metadata["artist"],),)

    if not len(metadata["title"]) > 3:
        sql += " WHERE song.title LIKE %s"
        args += ("%%%s%%" % (metadata["title"],),)

    if "album" in metadata and metadata["album"] is not None and not len(metadata["album"]) > 3:
        sql += " WHERE album.name LIKE %s"
        args += ("%%%s%%" % (metadata["album"],),)

    sql += " ORDER BY score DESC LIMIT 1"

    c.execute(sql, args)
    return c.fetchone()
