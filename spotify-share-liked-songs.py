#! /usr/bin/env python3

from Prints import printIntroduction
from Prints import printConclusion
from GetEnv import getValueOfVar

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def addTracksToPlaylist(playlist_id, items):
    n = 0

    while (n < len(items)):
        sp.playlist_add_items(playlist_id=playlist_id, items=toAdd[n:n+100])
        n += 100

def removeTracksFromPlaylist(playlist_id, items):
    n = 0

    while (n < len(items)):
        sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_id, items=toAdd[n:n+100])
        n += 100

def getPlaylistPublicLikedSongs():
    global sp

    playlists = sp.current_user_playlists()
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if playlist['name'] == 'My liked songs':
                return playlist
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return None


def getAllLikedSongs():
    global sp
    liked_songs: list = []
    tmp: list = sp.current_user_saved_tracks(limit=50, offset=0)['items']
    offset: int = len(tmp)

    while len(tmp) != 0:
        for i in range(0, len(tmp)):
            liked_songs.append(tmp[i]['track']['id'])
        if len(tmp) != 50:
            break
        offset += len(tmp)
        tmp = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
    return liked_songs


def getSongsOfPlaylist(playlist):
    global sp
    res = []
    songs: List = sp.playlist_tracks(playlist['id'], limit=50, offset=0)['items']
    offset: int = len(songs)

    while len(songs) != 0:
        for i in range(0, len(songs)):
            if (songs[i]['track']['id'] is not None):
                res.append(songs[i]['track']['id'])
        if (len(songs) != 50):
            break
        offset += len(songs)
        songs = sp.playlist_tracks(playlist['id'], limit=50, offset=offset)['items']
    return res


printIntroduction()
print("Getting the Spotify API secrets...")
CLIENT_ID = getValueOfVar("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = getValueOfVar("SPOTIFY_CLIENT_SECRET")
user_id = None

if not CLIENT_SECRET or not CLIENT_ID:
    print("You need to add a .env file with your client id and secret. See -h")
    exit(84)

try:
    print("Connecting to the Spotify API...")
    scope = "playlist-modify-public user-library-read"
    redirect_uri = 'http://localhost:8888/callback/'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))

    print("Is already there a public playlist for your liked songs...")
    playlist_liked_songs_public = getPlaylistPublicLikedSongs()
    if playlist_liked_songs_public is None:
        print("Can't find it")
        description = 'This is an automatic added playlists by the spotify-share-liked-songs program. ' \
                      + ' (source code available on github)'
        user_id = sp.current_user()['id']
        print("Creating a public playlist for your liked songs...")
        sp.user_playlist_create(user_id, 'liked_songs_public', True, False, description)
        playlist_liked_songs_public = getPlaylistPublicLikedSongs()
    else:
        print("Found it!")
    if playlist_liked_songs_public is None:
        print('Something went wrong...')
        exit(84)

    print("Getting your liked songs...")
    liked_songs = getAllLikedSongs()
    print("Getting the songs in the public playlist...")
    liked_songs_public = getSongsOfPlaylist(playlist_liked_songs_public)

    print("Determining the songs to be added...")
    toAdd = []
    for song in liked_songs:
        if song not in liked_songs_public:
            toAdd.append(song)
    print("Determining the songs to be removed...")
    toDelete = []
    for song in liked_songs_public:
        if song not in liked_songs:
            toDelete.append(song)

    print("Adding liked songs to your public playlist...")
    addTracksToPlaylist(playlist_id=playlist_liked_songs_public['id'], items=toAdd)
    print("Removing old liked songs from your public playlist...")
    removeTracksFromPlaylist(playlist_id=playlist_liked_songs_public['id'], items=toDelete)
    print("Done!")

except Exception as error:
    print("ERROR: " + str(error))
    exit(84)
printConclusion()
