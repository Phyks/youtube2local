"""
Checks if a song exist against Ampache SQL database directly.
"""
import MySQLdb
import MySQLdb.cursors

def check(str, config):
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
