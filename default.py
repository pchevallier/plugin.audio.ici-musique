import os
import sys
import urllib.parse as urlparse
from datetime import datetime
import xbmcgui
import xbmcplugin
import xbmc

def set_file_constant(file):
    file_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(file_path, "resources", file)

MONITOR = xbmc.Monitor()
PLAYER = xbmc.Player()
ADDON_HANDLE = int(sys.argv[1])
ID = "plugin.audio.ici-musique"
ICON = set_file_constant("icon.png")
FANART = set_file_constant("fanart.jpg")

PROGRAM = None
PROGRAM_SCHEDULE = None
TRACK = None
PLAYLOG = None
KEY = None
LOCATION = None

def list_streams(stn):
    xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}: list_streams: {stn}")                                                                                                                                                                                                                   
    url='plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Frcavliveaudio.akamaized.net%2Fhls%2Flive%2F2006979%2FM-7QMTL0_MTL%2Fadaptive_192%2Fchunklist_ao.m3u8&title=ICI+Musique+-+Montreal&key=2&location=montreal'              
                                                                                                                                                                                                                                          
    station_and_title = "ICI Musique - Montreal"                                                                                                                                                                                
    li = xbmcgui.ListItem(station_and_title)                                                                                                                                                                                    
    li.setProperty("IsPlayable", "true")                                                                                                                                                               
    li.setArt({"icon": ICON, "fanart": FANART})                                                                                                                                                        
    xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li)  
    xbmcplugin.endOfDirectory(ADDON_HANDLE)

def update_play_item():
    global PROGRAM
    global PROGRAM_SCHEDULE
    global TRACK
    global PLAYLOG
    update = False
    try:
        play_item = PLAYER.getPlayingItem()
        tag = PLAYER.getMusicInfoTag()
        #xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}::update_play_item(): {tag.getTitle()}")
    except RuntimeError:
        xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}::update_play_item(): creating new ListItem")
        play_item = xbmcgui.ListItem()
        tag = xbmc.InfoTagMusic()
        update = True
    if not PLAYLOG:
        info_labels = {
            'artist': '',
            'title': ''
            }
        play_item.setArt({'thumb': ICON})
    else:
        info_labels = {
            'album': TRACK.album,
            'artist': TRACK.artist,
            'title': TRACK.title
            }
        play_item.setArt({'thumb': TRACK.cover_url})
    try:
        if update:
            #play_item.setArt({'thumb': TRACK.cover_url})
            play_item.setInfo('music', info_labels)
            PLAYER.updateInfoTag(play_item)
            #xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}::update_play_item(): {tag.getTitle()}")
        return play_item
    except RuntimeError:
        return play_item



def chill(length):
    MONITOR.waitForAbort(length)
    if MONITOR.abortRequested():
        PLAYER.stop()

def initialize(url):
    play_item = update_play_item()
    play_item.setPath(url)
    play_item.setProperty('IsPlayable', 'true')
    play_item.addStreamInfo('audio', {'codec': 'aac', 'channels': 2})
    if PLAYER.isPlaying():
        PLAYER.stop()
        chill(1)
    xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, listitem=play_item)
    while not PLAYER.isPlaying() or xbmc.getCondVisibility('Window.IsActive(BusyDialog)'):
        chill(1)
        xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}: sleep for fullscreen")
    xbmc.executebuiltin('Action(FullScreen)')
    xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}: fullscreen")

def play_stream(url):
    initialize(url)
    while not MONITOR.abortRequested():
        #update_play_item()
        chill(5)
        if not PLAYER.isPlaying():
            sys.exit(0)

def list_stations():                                                                                                                                                                                   
    url = 'plugin://plugin.audio.ici-musique/?mode=folder&foldername=Ici+Musique'                                                                                                                         
    station = 'ICI Musique'                                                                                                                                                                            
    li = xbmcgui.ListItem(station)                                                                                                                                                                     
    xbmcplugin.addDirectoryItem(                                               
        handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True               
    )                                                                                                                                                        
    xbmcplugin.endOfDirectory(ADDON_HANDLE)                                             

def main():

    args = urlparse.parse_qs(sys.argv[2][1:])
    mode = args.get("mode", None)

    if mode is None:
        list_stations()

    elif mode[0] == "folder":
        station = args["foldername"][0]
        list_streams(station)

    elif mode[0] == "stream":
        url = args["url"][0]
        global KEY
        KEY = int(args["key"][0])
        global LOCATION
        LOCATION = args["location"][0]
        play_stream(url)
        sys.exit(0)


if __name__ == "__main__":
    main()