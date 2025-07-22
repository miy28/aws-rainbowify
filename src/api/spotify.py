import os
import sys
import requests

from src.data.models import UserLikedSongs

'''
create a new .txt file called 'credentials.txt'
paste your Spotify client ID in the first line
paste your Spotidy client client secret in the second line
'''
this_dir = os.path.dirname(__file__)
cred_path = os.path.join(this_dir, 'spotify_credentials.txt')

with open(cred_path, 'r') as f:
    client_id = f.readline().strip()
    client_secret = f.readline().strip()

'''
generator function that calls GET/me/tracks Spotify API until all user liked songs have been stored into datamodel.

params:
    access_token: Spotify API access token
yields:
    dict: current track metadata.
'''
def iterate_liked_songs(access_token):
    track_ids = []
    
    limit = 50
    offset = 0
    
    while True:
        url = f'https://api.spotify.com/v1/me/tracks?limit={limit}&offset={offset}'
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(url, headers=headers)
        if not response.ok:
            print(f"\n\nError fetching Spotify data: {response.status_code}\n")
            return

        response_json = response.json()
        items = response_json.get('items', [])
        
        # get track ids from items list
        track_ids_lim = []
        for item in items:
            track = item.get('track', {})

            track_id = track.get('id')
            track_name = track.get('name')
            track_addedAt = track.get('added_at')
            track_duration = track.get('duration')
            
            yield { # iterable return. mem efficient
                'id': track_id,
                'track_name': track_name,
                'added_at': track_addedAt,
                'track_duration': track_duration,
                'full_item': item
            }

            track_ids_lim.append(track_id)
        
        track_ids.extend(track_ids_lim)

        if len(items) < limit: # check if reached end of user's liked songs
            break
            
        offset += limit
    
    # push to RDS mySQL here
    
    return track_ids

'''
requests user authorization for their spotify account
'''
def get_user_auth(client_id: str, redirect_uri: str):
    from urllib.parse import urlencode

    url = 'https://accounts.spotify.com/authorize'
    state = ''

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'state': state,
        'scope': 'playlist-read-private user-library-read'
    }

    # response = requests.get(url, params=params)

    # if not response.ok:
    #     print(f"Error fetching user authorization: {response.status_code}")
    #     return None

    # return response.url

    url = f"{url}?{urlencode(params)}"

    return url

'''
gets temporary access token
'''
def get_access_token(client_id: str, client_secret: str, code: str, redirect_uri: str):
    url = "https://accounts.spotify.com/api/token" # -X

    headers = { # -H
        "content-type": "application/x-www-form-urlencoded"
    }

    data = { # -d
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        'redirect_uri': redirect_uri
    }

    response = requests.post(url, headers=headers, data=data) # POST request to get valid (1 hr) access token

    if not response.ok:
        print(f"Error fetching access token: {response.status_code}")
        return None

    access_token = response.json().get("access_token")

    return access_token