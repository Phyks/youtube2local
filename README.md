Youtube2local
=============

This is a script to help you match Youtube music videos and playlists with
your local song collection.


## Usage

* Install the required dependencies: `pip install -r requirements.txt`.
* Copy and edit the `config.py.example` file to `config.py` according to your
  needs.
* Run the script: `python3 -m youtube2local "https://www.youtube.com/watch?v=1mkUp1V3ys0"`.


## Extending backends

For now it only features a backend using the database from an Ampache
installation. You can easily extend backends by adding files in the `backends`
directory, implementing the `check` function as the `ampacheSQL.py` backend
does. Then, just edit your config accordingly.

Feel free to submit any PR for new backends.


## LICENSE

Released under MIT license.
