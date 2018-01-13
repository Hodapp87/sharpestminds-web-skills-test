#!/usr/bin/env python

###########################################################################
# scrape.py: Web skills test module to scrape setlist.fm for artist info 
# Author: Chris Hodapp (hodapp87@gmail.com)
# Date: 2018-01-12
###########################################################################

import json
import requests
#import bs4

BASE_URL = "https://api.setlist.fm/rest/1.0"

# Request headers sent with every API call:
headers = {
    # API key is hard-coded (bad practice, but it's allowed in the
    # other Python module too):
    "x-api-key": "7445bfb6-4ab8-4900-9929-59bfaec097f0",
    # We only want JSON results:
    "Accept": "application/json",
}

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
    # TODO: Handle 'resp' return codes
    print(resp.status_code)
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
    set_ = resp.json()["setlist"][0]
    print(json.dumps(set_, indent=4, sort_keys=True))
    songs = [d["name"] for d in set_["sets"]["set"][0]["song"]]
    return songs
