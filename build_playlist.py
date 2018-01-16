#!/usr/bin/env python

###########################################################################
# build_playlist.py: Web skills test module to make playlist for an artist
# Author: Chris Hodapp (hodapp87@gmail.com)
# Date: 2018-01-12
###########################################################################

import sys

import scrape
import spotify
import spotipy

def create_playlist(artist):
    """Create a Spotify playlist containing the latest songs by the given
    artist, and print a link to this playlist.

    Parameters:
    artist -- String containing a musician or band name
    """
    songs = scrape.find_songs(artist)
    print("Using list of songs:")
    for i,song in enumerate(songs):
        print("{}. {}".format(i, song))
    print("Creating playlist on Spotify...")
    url = spotify.generate_playlist(songs)
    print("Playlist URL: {}".format(url))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <artist name>".format(sys.argv[0]))
        print("This will use setlist.fm to retrieve the latest setlist from the")
        print("given artist, create a Spotify playlist with the tracks from that")
        print("setlist, then print the public URL to that playlist.")
        sys.exit(1)
    try:
        artist = sys.argv[1]
        create_playlist(artist)
        sys.exit(0)
    except scrape.SetListHTTPException as e:
        print("HTTP status {} when accessing setlist.fm".format(e.status))
        sys.exit(2)
    except scrape.SetListNotFoundException:
        print("Unable to find setlist for artist {}".format(artist))
        sys.exit(3)
    except spotipy.oauth2.SpotifyOauthError as e:
        print("Error authenticating with Spotify: {}".format(e))
        sys.exit(4)
    except spotipy.SpotifyException as e:
        print("Error with Spotify: {}".format(e))
        sys.exit(5)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Error: {}".format(e))
        sys.exit(6)
