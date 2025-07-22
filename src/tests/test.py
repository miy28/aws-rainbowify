import os

from src.api.spotify import iterate_liked_songs, get_user_auth, get_access_token
from src.data.models import UserLikedSongs

this_dir = os.path.dirname(__file__)
cred_path = os.path.join(this_dir, 'spotify_credentials.txt')

'''
create a new .txt file called 'credentials.txt'
paste your Spotify client ID in the first line
paste your Spotidy client client secret in the second line
'''
with open(cred_path, 'r') as f:
    client_id = f.readline().strip()
    client_secret = f.readline().strip()

if __name__ == "__main__":
    print("please authenticate your spotify account here:\n", get_user_auth(client_id))
    auth_code = input("paste the code here: ").strip()
    token = get_access_token(client_id, client_secret, auth_code)
    tracks = iterate_liked_songs(token)
    for track in tracks:
        id = track.get('track_name')
        print(id)