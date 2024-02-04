# Handles the execution of our program

import youtube
import spotify

# Runs the program without an user interface (using default values in secret.py)
def run():
    songs = youtube.get_songs()
    spotify.create_playlist(songs)

    print()
    print("Playlist created! Check your spotify account.")
    print()

if __name__ == "__main__":
    run()