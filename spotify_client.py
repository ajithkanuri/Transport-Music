import requests
import urllib.parse as ur

class SpotifyClient(object):
    def __init__(self,apitoken):
        self.api_token = apitoken
    #search for songs
    def search_song(self, artist, track):
        query = ur.quote(f'{artist} {track}')
        url = f'https://api.spotify.com/v1/search?q={query}&type=track'
        response = requests.get(
            url,
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"            
                }
        )
        response_json = response.json()
        results = response_json['tracks']['items']
        if results:
            return results[0]['id']
        else:
            raise Exception(f'No song found for {artist} = {track}')


    def add_song_to_spotify(self, song_id):
        url = "https://api.spotify.com/v1/me/tracks"
        response = requests.put(
            url, 
            json={
                'ids': [song_id]

            },
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"            
                }

        )
        return response.ok
        

    
