#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import webbrowser

uri = '7qiZfU4dY1lWllzX7mPBI3'
urlauth = 'https://accounts.spotify.com/api/token'
urlsรถk = 'https://api.spotify.com/v1/tracks/' + uri

body_params = {'grant_type':'client_credentials'}
client_id = 'fecdb57f9c9c49d58e7bd63841773fc7'
client_secret = '7a3a4a896838424c9df8e8cef6b543fd'

tokeninfo = requests.post(urlauth,data=body_params,auth=(client_id,client_secret)).json()

id = 'Bearer ' + tokeninfo['access_token']
info = requests.get(urlsรถk,headers={'Authorization':id}).json()

track = info['preview_url']
namn = info['name']

if track:
    print("Spelar",namn)
    webbrowser.open(track)
    
else:
    print('Ingen förhandslyssning av',namn)

#dbus("--print-reply","--dest=org.mpris.MediaPlayer2.spotify","/org/mpris/MediaPlayer2","org.mpris.MediaPlayer2.Player.OpenUri","string:spotify:track:2TpxZ7JUBn3uw46aR7qd6V")
#nyckel(b64) = 'ZmVjZGI1N2Y5YzljNDlkNThlN2JkNjM4NDE3NzNmYzc6N2EzYTRhODk2ODM4NDI0YzlkZjhlOGNlZjZiNTQzZmQ='

