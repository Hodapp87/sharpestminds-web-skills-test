#!/usr/bin/env python

###########################################################################
# spotify.py: Web skills test module to create a Spotify playlist
# Author: Chris Hodapp (hodapp87@gmail.com)
# Date: 2018-01-12
###########################################################################

import scrape
import spotipy
import spotipy.util

token = spotipy.util.prompt_for_user_token(
    "hodapp",
    "playlist-modify-private",
    client_id = "caaa12900a34490dbba42487f4f37923",
    client_secret = "ada72b869ccf4cf4afb16560d95c956c",
    redirect_uri = "http://localhost:8888/callback?code=AQC5dPffRz09FPxhjLqhqBjejo4jIqUlH9VmZanq-qSkqGVhFYroZ0FbuUxTUOVnpDdqHIxyCqvd3MYPk9EbJJ38dyH1z5r120pvPWZE6cESdDsOxxbqnPD1vFt9Bd4tawqhY9avBLotbn-UfIUJ2Tixr8CuCmBME4UGgoQngHvkrdRqJhGcHUkK-EBt_wPi2b2NUp3BDeHbqBdrk6LZ-RNz-ezBmztsGxlFZSg")

# sp = spotipy.Spotify(auth=token)
# sp.user_playlist_create
# sp.user_playlist_add_tracks

def generate_playlist(songs):
    """Given a list of songs, creates a Spotify playlist which contains
    those songs, and returns a link to this playlist.

    Parameters:
    songs -- A list of song names (given as strings)

    Returns:
    playlist_link -- A link to a Spotify playlist
    """
    pass
