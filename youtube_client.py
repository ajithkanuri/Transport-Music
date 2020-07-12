import os
import json
import google_auth_oauthlib.flow
import googleapiclient.errors
import requests
import googleapiclient.discovery
import youtube_dl
class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track  = track
class Playlist(object):
    def __init__(self, id, title):
        self.id = id 
        self.title = title
class YouTubeClient(object):
    def __init__(self, cred_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        # client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
        cred = 'client_secret_876125188595-50gj6lg8jgev9naok6gt7282cr3q5ll0.apps.googleusercontent.com.json'
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            cred, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.youtube_client= youtube_client
    
    def get_playlists(self):
        request = self.youtube_client.playlists().list(
            part="id, snippet",
            maxResults=50,
            mine=True
        )
        response = request.execute()
        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]
        return playlists

    def get_videos_from_playlist(self, playlist_id):
        request = self.youtube_client.playlistItems().list(
            playlistId= playlist_id,
            part = 'id, snippet',
            maxResults = 50
        )
        songs = []
        reponse = request.execute()
        for item in reponse['items']:
            video_id = item['snippet']['resourceId']['videoId']
            artist,track = self.get_artist_and_track_from_vid(video_id) 
            if artist and track:
                songs.append(Song(artist,track))

        return songs
    def get_artist_and_track_from_vid(self, video_id):
        youtube_url = f"http://www.youtube.com/watch?v={video_id}"

        video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(youtube_url, download= False)
        artist = video['artist']
        track = video['track']
        return (artist, track)