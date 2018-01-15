#!/usr/bin/env python

###########################################################################
# build_playlist.py: Web skills test module to make playlist for an artist
# Author: Chris Hodapp (hodapp87@gmail.com)
# Date: 2018-01-12
###########################################################################

import sys

import scrape
import spotify

def create_playlist(artist):
    """Create a Spotify playlist containing the latest songs by the given
    artist, and print a link to this playlist.

    Parameters:
    artist -- String containing a musician or band name
    """
    songs = scrape.find_songs(artist)
    url = spotify.generate_playlist(songs)
    print(url)
