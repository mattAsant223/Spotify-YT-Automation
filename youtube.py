# Handles the interaction with the YouTube Data API

from urllib.parse import quote

from secret import PLAYLIST_ID

# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    

# Get the song information from each video in the given Youtube playlist
def get_songs():
    videos = get_videos_from_playlist()

    # Get the song info of each video in the playlist from its video title
    songs = []
    for video in videos["items"]:
        song_info = extract_song_info(video["snippet"]["title"])
        songs.append(song_info)

    return songs

# Returns the list of videos from the playlist id specified in the secret.py file
def get_videos_from_playlist():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId= PLAYLIST_ID
    )
    response = request.execute()

    return response

    


# Given a video title, return the corresponding song information
# e.g. For the video title "Miley Cyrus - Party In The USA", return:
# {
#     artist: "Miley%20Cyrus"
#     song: "Party%20In%20The%20USA"
# }
def extract_song_info(video_title):
    info = video_title.split("-")
    artist_name = quote(info[0].strip(), safe = '')
    song_name = quote(info[1].strip(), safe = '')

    return {
        "artist": artist_name,
        "song": song_name
    }