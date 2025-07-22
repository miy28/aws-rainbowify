from flask import Flask, redirect, request, session, url_for, jsonify
import os
from src.api.spotify import get_user_auth, get_access_token, iterate_liked_songs, client_id, client_secret

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your_secret_key")

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", client_id)
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", client_secret)
REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:3000/callback")

@app.route("/")
def index():
    return '<a href="/login">Login with Spotify</a>'

@app.route("/login")
def login():
    # Use get_user_auth to generate the Spotify auth URL
    auth_url = get_user_auth(CLIENT_ID, REDIRECT_URI)
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "No code provided", 400

    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, code, REDIRECT_URI)
    if not access_token:
        return "Failed to get access token", 400

    session["access_token"] = access_token

    return redirect(url_for("liked_songs"))

@app.route("/liked_songs")
def liked_songs():
    access_token = session.get("access_token")
    
    if not access_token:
        return redirect(url_for("login"))
    
    track_names = [track["track_name"] for track in iterate_liked_songs(access_token)]

    return jsonify(track_names)

if __name__ == "__main__":
    app.run(debug=True, port=3000)