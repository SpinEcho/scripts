#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
import spotipy
import spotipy.util as util


class SpotifySearch:
    def __init__(self, master):
        # Spotifyinloggning
        self.client_id = 'fecdb57f9c9c49d58e7bd63841773fc7'
        self.client_secret = '7a3a4a896838424c9df8e8cef6b543fd'
        self.scope = 'playlist-modify-private playlist-read-private'
        self.user = 'spinecho'
        self.redirect_uri = 'http://example.com/callback/'
        self.token = util.prompt_for_user_token(self.user, self.scope, self.client_id, self.client_secret,
                                                self.redirect_uri)
        self.sp = spotipy.Spotify(auth=self.token)

        # Spotifyvariabler
        self.offset = 0
        self.temp_list = []
        self.track_list = []
        self.next = True

        # Layoutvariabler
        self.widgetfont = ('helvetica', 14)

        # Layout
        self.master = master
        master.title('SpotifySearch')
        master.geometry('400x200')

        self.frame1 = Frame(master)
        self.frame1.pack(fill=X)

        self.frame2 = Frame(master)
        self.frame2.pack(fill=X)

        self.frame3 = Frame(master)
        self.frame3.pack(fill=X)

        self.label1 = Label(self.frame1, text='Artist:')
        self.label1.configure(font=self.widgetfont)
        self.label1.pack(side='left', pady=10)

        self.inmatning = Entry(self.frame1)
        self.inmatning.bind('<Return>', self.search_add)
        self.inmatning.focus()
        self.inmatning.pack(side='left')

        self.label2 = Label(self.frame2)
        self.label2.configure(font=self.widgetfont)
        self.label2.pack(side='left')

        self.label3 = Label(self.frame3)
        self.label3.configure(font=self.widgetfont)
        self.label3.pack(side='left')

    def search_add(self, event):
        self.artist = self.inmatning.get()
        self.inmatning.delete(0, 'end')
        self.playlist = self.sp.user_playlist_create(self.user, self.artist + '_top20', public=False)
        self.playlist_id = self.playlist['id']
        self.label2.configure(text='Skapat spellistan ' + self.artist + '_top20')

        self.search()
        self.arrange()

        self.sp.user_playlist_add_tracks(self.user, self.playlist_id, self.track_list)
        self.label3.configure(text='Lagt till låtar')

    def search(self):
        if self.next:
            self.track_result = self.sp.search(q='artist:' + self.artist, limit=50, offset=self.offset, type='track',
                                               market='SE')
            self.track_hits = self.track_result['tracks']['items']
            for tracks in self.track_hits:
                self.temp_list.append([tracks['uri'], tracks['popularity']])

            if self.track_result['tracks']['next']:
                self.offset += 50

            else:
                self.next = False

    def arrange(self):
        self.temp_list.sort(key=lambda x: x[1], reverse=True)
        if len(self.temp_list) > 20:
            self.temp_list = self.temp_list[:20]

        for track in self.temp_list:
            self.track_list.append(track[0])


root = Tk()
MyApp = SpotifySearch(root)
root.mainloop()
