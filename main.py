import json
import requests
from secrets import spotify_user_id
from refresh import Refresh


class DateRangeSongs:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.albums = ""
        self.new_playlist_id = ""
        self.tracks = ""

    def get_albums_tracks(self):
        print("Finding artist's albums: ")
        artist_id = input("Enter artist's URI: ")
        artist_id = artist_id[15:]
        startYear = input("Enter a year to start from: ")
        print("Getting tracks: ")
        query = "https://api.spotify.com/v1/artists/{}/albums".format(artist_id)
        albums = []

        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)},
                                params={"include_groups": "album", 'limit': 50
                                        })

        response = response.json()

        for album in response["items"]:

            album_name = album['name']

            trim_name = album_name.split('(')[0].strip()

            if trim_name.upper() in albums or int(album["release_date"][:4]) < int(startYear):
                continue
            albums.append(trim_name.upper())

            trackQuery = requests.get("https://api.spotify.com/v1/albums/" + album['id'] + "/tracks",
                                      headers={"Content-Type": "application/json",
                                               "Authorization": "Bearer {}".format(self.spotify_token)})

            tracks = trackQuery.json()["items"]

            for i in tracks:
                self.tracks += (i["uri"] + ",")
        self.tracks = self.tracks[:-1]

        self.add_to_playlist()
        # print(response_json)

        # for album in response_json['items']:
        #    self.albums += (album["id"] + ",")
        # self.albums = self.albums[:-1]

        # print(self.albums)

        # self.get_album_tracks()

    # def get_album_tracks(self):
    #     print("Getting album tracks")

    #    query = "https://api.spotify.com/v1/albums/{}/tracks".format(self.albums)

    #    response = requests.get(query,
    #                            headers={"Content-Type": "application/json",
    #                                     "Authorization": "Bearer {}".format(self.spotify_token)},
    #                            params={"market": "US"})

    #    response_json = response.json()

    #    for i in response_json["items"]:
    #        self.tracks += (i["tracks"]["uri"] + ",")
    #    self.tracks = self.tracks[:-1]

    #    self.add_to_playlist()

    def create_playlist(self):
        print("Creating playlist..")

        playlistName = input("Enter a playlist name: ")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)

        request_body = json.dumps({
            "name": playlistName, "public": False
        })

        response = requests.post(query, data=request_body, headers={"Content-Type": "application/json",
                                                                    "Authorization": "Bearer {}".format(
                                                                        self.spotify_token)

                                                                    })

        response_json = response.json()

        return response_json["id"]

    def add_to_playlist(self):
        print("Adding songs to playlist")

        self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)

        response = requests.post(query, headers={"Content-Type": "application/json",
                                                 "Authorization": "Bearer {}".format(self.spotify_token)

                                                 })

        print(response.json)

    def call_refresh(self):
        print("Refreshing token..")

        refreshCaller = Refresh()

        self.spotify_token = refreshCaller.refresh()

        self.get_albums_tracks()


a = DateRangeSongs()
a.call_refresh()
