#!/usr/bin/env python

###########################################################################
# scrape.py: Web skills test module to scrape setlist.fm for artist info 
# Author: Chris Hodapp (hodapp87@gmail.com)
# Date: 2018-01-12
###########################################################################

import requests
import bs4

def find_songs(artist):
    """Obtains the songs from a musical artist's latest set-list.  This
    scrapes http://www.setlist.fm in order to get this data.

    Parameters:
    artist -- String with the musician or band's name

    Returns:
    songs -- A list of song names (as strings)
    """
    pass
