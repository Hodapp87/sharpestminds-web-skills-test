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

BASE_URL = "https://api.setlist.fm/rest/1.0"

# Request headers sent with every API call:
headers = {
    # API key is hard-coded (bad practice, but it's allowed in the
    # other Python module too):
    "x-api-key": "7445bfb6-4ab8-4900-9929-59bfaec097f0",
    # We only want JSON results:
    "Accept": "application/json",
}

def json_pprint(j):
    """Utility-function to pretty-print a parsed JSON tree."""
    print(json.dumps(j, indent=4, sort_keys=True))

def find_songs(artist):
    """Obtains the songs from a musical artist's latest set-list.  This
    scrapes http://www.setlist.fm in order to get this data.

    Parameters:
    artist -- String with the musician or band's name

    Returns:
    songs -- A list of song names (as strings)
    """
    # api.setlist.fm's API will return setlists for an artist, but the
    # artist must be given by its MusicBrainz ID.  Thus, we must first
    # query for artists, and receive most-relevant results first:
    params = {
        "artistName": artist,
        "sort": "relevance"
    }
    artist_url = BASE_URL + "/search/artists"
    resp = requests.get(artist_url, params, headers=headers)
    if resp.status_code != requests.codes.ok:
        raise SetListHTTPException(resp.status_code)
    # TODO: Check for non-zero list
    artist_dict = resp.json()["artist"][0]
    mbid = artist_dict["mbid"]
    # TODO: Make sure MBID looks like a GUID (we're inserting it into
    # a URL)
    name = artist_dict["name"]
    print("Found MusicBrainz ID {} for artist \"{}\"".format(mbid, name))
    
    # Then, query for the latest setlist:
    setlist_url = BASE_URL + "/artist/" + mbid + "/setlists"
    resp = requests.get(setlist_url, headers=headers)
    if resp.status_code != requests.codes.ok:
        raise SetListHTTPException(resp.status_code)
    # TODO: Do results come back newest-first?
    # TODO: Check for non-empty set-list
    set_ = resp.json()["setlist"][0]
    json_pprint(set_)
    songs = [d["name"] for d in set_["sets"]["set"][0]["song"]]
    # See the artist Pavement for an example where "set" has multiple
    # elements (in this case, for their encore)
    return songs
