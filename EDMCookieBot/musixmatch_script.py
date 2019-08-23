#!/usr/bin/env python

import time
import sys
import json
import random
from pprint import pprint
import config_script

#generates snippet, returns snippet and artist name
def generate_fortune():
    fortune_array = []
    snippet_not_generated = True
    #keep looping until a valid snippet is found
    while snippet_not_generated:
        snippet_not_generated = False
        artist = get_random_artist()
        print('artist')
        print(artist)
        album = get_random_album(artist)
        print('album')
        print(album)
        try:
            track = get_random_track(album)
            if track == 'not found':
                snippet_not_generated = True
                continue
        except:
            print('***track not found, retrying...')
            snippet_not_generated = True
            continue

        snippet = get_random_snippet(track)
        print('snippet')
        print(snippet)
        if snippet == 'not found':
            snippet_not_generated = True
            continue
        artist_name = lookup_artist_name(artist)
        song_name = lookup_song_name(track)
        fortune_array.append(artist_name)
        fortune_array.append(snippet.body)
        fortune_array.append(song_name)
        print(fortune_array)
        return fortune_array

#returning artist name
def lookup_artist_name(artist_id):
    res = artist_api.artist_get_get(artist_id)
    return res.message.body.artist.artist_name

#returning song name
def lookup_song_name(track_id):
    track = track_api.track_get_get(track_id)
    return track.message.body.track.track_name

#returns a random artist from hardcoded array (generated from other get_artist_ids.py)
def get_random_artist():
    artist_ids = [26575484, 13819643, 14015300, 58366, 27756169, 173916, 28713090, 26490468, 461650, 475281, 33491423, 12992681, 27913594, 22115, 13828899, 142303, 13778283, 13996061, 13816078, 24513808, 33491981, 100076, 24407895, 28849994, 24403590, 28902287, 24450367, 13777655, 397519, 24393203, 27795670, 24513808, 33491981, 100076, 24407895, 28849994, 24403590, 28902287, 24450367, 13777655, 397519, 24393203, 27795670]
    random_artist = artist_ids[random.randrange(0, len(artist_ids)-1)]
    return random_artist

#returns a random album by designated artist
def get_random_album(artist_id):
    album_res = album_api.artist_albums_get_get(artist_id=artist_id, format=format)
    album_size = len(album_res.message.body.album_list)
    # pprint(album_res.message.header.available)
    random_album_index = random.randrange(0, album_size-1)
    random_album = album_res.message.body.album_list[random_album_index].album.album_id
    return random_album

#returns a random track from designated album
def get_random_track(album_id):
    #using musixmatch wrapper since the original python sdk doesn't work
    tracks = musixmatch.album.tracks(album_id, page_size=10, has_lyrics=True)
    # print(tracks[0].track_id)
    track_size = len(tracks)
    if track_size == 0:
        return 'not found'
    if track_size == 1:
        random_track_index = 0
    else:
        random_track_index = random.randrange(0, track_size-1)

    random_track = tracks[random_track_index].track_id
    print(tracks[random_track_index].track_name)
    print(tracks[random_track_index].album_name)
    # pprint(random_track)
    return random_track

#returns snippet from track
def get_random_snippet(track_id):
    snippet = musixmatch.track.snippet(track_id)
    print('hehe')
    print(snippet.body)
    # print(snippet.body.snippet)
    if snippet.body == 'None' or snippet.body == '' or snippet.body is None:
        return 'not found'
    # print(snippet)
    return snippet

#initializing clients and APIs
swagger_client = config_script.create_swagger_client()
musixmatch = config_script.create_musixmatch_api()
album_api = swagger_client.AlbumApi()
artist_api = swagger_client.ArtistApi()
track_api = swagger_client.TrackApi()
format = 'json'
