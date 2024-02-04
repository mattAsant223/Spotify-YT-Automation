# Handles the interaction with the Spotify Web API

import requests
import base64
from urllib.parse import urlencode
import webbrowser

from secret import CLIENT_ID, CLIENT_SECRET, USER_ID, REDIRECT_URI

# Create the playlist with the given songs
def create_playlist(songs):
    pass
    # Obtain the access token to be able to use Spotify Web API
    access_token = get_user_permission()

    # Find the Spotify tracks closest to the information we got from YouTube
    track_uris = get_track_uris(songs, access_token)

    # Create a new playlist on Spotify
    new_playlist_id = create_new_playlist(access_token)

    # Populate the new playlist with the Spotify tracks we found
    populate_playlist(track_uris, new_playlist_id, access_token)

# Get permission from the user to make changes to their account by obtaining
# an authorization token. Follow the Authorization Code Flow. 
def get_user_permission():
    
    # Open a web browser to redirect the user and obtain the authorization code
    query = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "playlist-modify-private"
    }

    # NOTE: The full version of this URL would look like:
    # https://accounts.spotify.com/authorize?client_id=CLIENT_ID&response_type=code&redirect_uri=REDIRECT_URI&scope=playlist-modify-private
    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(query))

    # Prompt the user to enter the authorization code after being redirected
    auth_code = input("After authorizing this application, enter the authorization code: ")
    
    
    
    # Use the access code to get the access token
    # Make a POST request to the /token endpoint to get an access token
    url = "https://accounts.spotify.com/api/token"
    auth_header = base64.urlsafe_b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode())
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic {}".format(auth_header.decode("ascii"))
    }
    body = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(url, data=body, headers=header)

    print(response.json()["access_token"])
    return response.json()["access_token"]
    

# Get the Spotify URI of each track
def get_track_uris(songs, token):
    
    # Obtain the base url for us to insert song information into
    base_url = "https://api.spotify.com/v1/search?q=remaster%2520track%3A{}%2520artist%3A{}&type=track"

    # Go through each of the songs and find the corresponding spotify uri
    track_uris = []
    for track in songs:
        # Send a GET request to the /search endpoint retreive the song info
        url = base_url.format(track["song"], track["artist"])
        header = {
            "Authorization": "Bearer {}".format(token)
        }
        response = requests.get(url, headers=header)

        # Obtain the URI of the track from the response and add it to the list
        uri = response.json()["tracks"]["items"][0]["uri"]
        track_uris.append(uri)
    
    # print(*track_uris, sep = ", ")
    return track_uris
    

def create_new_playlist(token):
    
    # Send a POST request to the /playlist endpoint create the playlist
    url = "https://api.spotify.com/v1/users/{}/playlists".format(USER_ID)
    head = {
        "Authorization": "Bearer {}".format(token), 
        "Content-Type": "application/json"
    }
    body = {
        "name": "YT PLAYLIST",
        "description": "man",
        "public": False,
        "collaborative": True
    } 
    response = requests.post(url, json=body, headers=head)

    print(response.json()["id"])
    return response.json()["id"]
    

# Creates a new playlist with the tracks from the given track_uris
def populate_playlist(track_uris, playlist_id, token):
    
    # Send a POST request to add the songs to the playlist
    url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
    head = {
        "Authorization": "Bearer {}".format(token), 
        "Content-Type": "application/json"
    }
    body = {
        "uris": track_uris,
        "position": 0
    }
    requests.post(url, json=body, headers=head)
    