#!/usr/bin/env python

###########################################################################
# scrape.py: Web skills test module to scrape setlist.fm for artist info 
# Author: Chris Hodapp (hodapp87@gmail.com)
# Date: 2018-01-12
###########################################################################

import json
import requests
#import bs4

class SetListHTTPException(Exception):
    """Custom exception class for an HTTP status that is not 200 (OK).
    """
    def __init__(self, status, *args, **kwargs):
        """Create a SetListHTTPException.  All other arguments besides
        'status' are passed on to Exception's constructor.

        Parameters:
        status -- Integer for HTTP status code

        """
        self.status = status
        Exception.__init__(self, *args, **kwargs)
    def __str__(self):
        return "HTTP status {}".format(self.status)

class SetListNotFoundException(Exception):
    pass
    
def json_pprint(j):
    """Utility-function to pretty-print a parsed JSON tree."""
    print(json.dumps(j, indent=4, sort_keys=True))

def find_songs(artist, base_url="https://api.setlist.fm/rest/1.0",
               api_key = "7445bfb6-4ab8-4900-9929-59bfaec097f0"):
    """Obtains the songs from a musical artist's latest set-list.  This
    scrapes http://www.setlist.fm in order to get this data.

    Parameters:
    artist -- String with the musician or band's name
    base_url -- Optional string with URL prefix for setlist.fm API
                (default: https://api.setlist.fm/rest/1.0)
    api_key -- Optional API key for api.setlist.fm

    Returns:
    songs -- A list of song names (as strings)
    """
    # Sent with every request to force JSON and to pass API key:
    headers = { "x-api-key": api_key, "Accept": "application/json" }
    # I can use the API's /1.0/search/setlists to search directly by
    # artist, but I have run into cases where this returns the wrong
    # artist first.  Searching the artist first, sorted by relevance,
    # then searching for setlists by MBID seems to work better.
    params = { "artistName": artist, "sort": "relevance" }
    artist_url = base_url + "/search/artists"
    resp = requests.get(artist_url, params, headers=headers)
    if resp.status_code != requests.codes.ok:
        raise SetListHTTPException(resp.status_code)
    artists = resp.json()["artist"]
    if len(artists) == 0:
        raise SetListNotFoundException()
    mbid = artists[0]["mbid"]
    name = artists[0]["name"]
    print("Best match: artist \"{}\", MusicBrainz ID {}".format(name, mbid))
    
    # Then, query for the latest setlist:
    setlist_url = base_url + "/artist/" + mbid + "/setlists"
    resp = requests.get(setlist_url, headers=headers)
    if resp.status_code != requests.codes.ok:
        raise SetListHTTPException(resp.status_code)
    setlists = resp.json()["setlist"]
    # The responses appear to come back newest-first, but nothing in
    # the documentation says this.
    setlist = []
    # Search through all the setlists for the first one with at least
    # one set with at least one song.
    for setlist in setlists:
        songs = []
        # Sets may contain multiple parts (encores seem to be shown
        # this way), but are still the same set, so append them all:
        for group in setlist["sets"]["set"]:
            songs += [d["name"] for d in group["song"]]
        # Take the first non-empty setlist we've found:
        if songs:
            break
    if not songs:
        return SetListNotFoundException()
    return songs
