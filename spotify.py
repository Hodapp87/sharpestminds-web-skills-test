#!/usr/bin/env python

###########################################################################
# spotify.py: Web skills test module to create a Spotify playlist
# Author: Chris Hodapp (hodapp87@gmail.com)
# Date: 2018-01-12
###########################################################################

import scrape
import spotipy
import spotipy.util
import datetime

SPOTIFY_USERNAME = "hodapp"
token = spotipy.util.prompt_for_user_token(
    SPOTIFY_USERNAME,
    "playlist-modify-public",
    client_id = "caaa12900a34490dbba42487f4f37923",
    client_secret = "ada72b869ccf4cf4afb16560d95c956c",
    redirect_uri = "http://localhost:8888/callback")

def generate_playlist(songs):
    """Given a list of songs, creates a Spotify playlist which contains
    those songs, and returns a link to this playlist.

    Parameters:
    songs -- A list of song names (given as strings)

    Returns:
    playlist_link -- A link to a Spotify playlist
    """
    sp = spotipy.Spotify(auth=token)
    
    # Query for Spotify's song IDs:
    song_ids = []
    for song in songs:
        r = sp.search('track:"{}"'.format(song), type="track")
        tracks = r["tracks"]["items"]
        if tracks:
            song_ids.append(tracks[0]["id"])
        else:
            print('Skipped "{}" because no Spotify match was found'.format(song))
 
    # Create a new playlist and get its URL and ID:
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Playlist name has date/time at the end to keep it unique
    playlist_name = "SharpestMinds test " + dt
    r = sp.user_playlist_create(SPOTIFY_USERNAME, playlist_name)
    print('Created playlist: \"{}\"'.format(playlist_name))
    playlist_id = r["id"]
    playlist_url = r["external_urls"]["spotify"]
    
    # Add songs to the playlist:
    sp.user_playlist_add_tracks(SPOTIFY_USERNAME, playlist_id, song_ids)
    
    return playlist_url
