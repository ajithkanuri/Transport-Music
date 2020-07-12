from youtube_client import YouTubeClient
from spotify_client import SpotifyClient
import os
def run():
    #get list of playlists
    youtube_client= YouTubeClient('./client_secret_876125188595-la35iddi3u0vnuejhksmaf4tnma4tgcp.apps.googleusercontent.com.json')
    spotify_client = SpotifyClient('BQAaHHx8oX1TR3CKCIsy4mrTCmf72-Sfq_9XadFMr61VnoxYAlc6OqwoqFFD5QIpCTUuO4bDIskRjkVvnEc3Cmp1s3AURkFp3E5Kq0OJLyzvvBGVn-EKdd_TBqU2D44rCaKGX5CF5csp1dVgnCWAbSfQmemTv6VhOm83UAJ5yTOFTDJgMIRvSdSKX299XdJTfQ')
   
    playlists = youtube_client.get_playlists()
    for index, playlist_title in enumerate(playlists):
        print(f'{index}: {playlist_title}')
    print(len(playlists))
    resp = int(input("Enter your choice: "))
    chosen_playlist = playlists[resp]
    print(f"You selected: {chosen_playlist.title}")
    #get songs from playlist
    songs = youtube_client.get_videos_from_playlist(chosen_playlist.id)
    print(f"Attempting to add: {len(songs)}")
    #search for songs in playlist
    for song in songs:
        spotify_song_id = spotify_client.search_song(song.artist, song.track)
        if spotify_song_id:
            added_song = spotify_client.add_song_to_spotify(spotify_song_id)
            if added_song:
                print(f"Added {song.artist}")
    
if __name__ == '__main__':
    run()
