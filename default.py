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
ICON = set_file_constant("icon.png")
FANART = set_file_constant("fanart.jpg")

radio_stations = [{'name':'ICI Musique','title':'Eastern','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Frcavliveaudio.akamaized.net%2Fhls%2Flive%2F2006979%2FM-7QMTL0_MTL%2Fadaptive_192%2Fchunklist_ao.m3u8&title=ICI+Musique+-+Montreal&key=2&location=montreal'},
                  {'name':'ICI Musique','title':'Mountain','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Frcavliveaudio.akamaized.net%2Fhls%2Flive%2F2006999%2FM-7AEDM0_EDM%2Fadaptive_192%2Fchunklist_ao.m3u8&title=ICI+Musique+-+Montreal&key=2&location=montreal'},
                  {'name':'ICI Musique','title':'Pacific','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Frcavliveaudio.akamaized.net%2Fhls%2Flive%2F2006996%2FM-7BVAN0_VAN%2Fadaptive_192%2Fchunklist_ao.m3u8&title=ICI+Musique+-+Montreal&key=2&location=montreal'},
                  {'name':'ICI Premiere','title':'Eastern','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Frcavliveaudio.akamaized.net%2Fhls%2Flive%2F2006635%2FP-2QMTL0_MTL%2Fadaptive_192%2Fchunklist_ao.m3u8&title=ICI+Musique+-+Montreal&key=2&location=montreal'},
                  {'name':'ICI Premiere','title':'Mountain','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Frcavliveaudio.akamaized.net%2Fhls%2Flive%2F2006949%2FP-2AEDM0_EDM%2Fadaptive_192%2Fchunklist_ao.m3u8&title=ICI+Musique+-+Montreal&key=2&location=montreal'},
                  {'name':'ICI Premiere','title':'Pacific','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Frcavliveaudio.akamaized.net%2Fhls%2Flive%2F2006975%2FP-2BVAN0_VAN%2Fadaptive_192%2Fchunklist_ao.m3u8&title=ICI+Musique+-+Montreal&key=2&location=montreal'},
                  {'name':'ICI Musique Classique','title':'Montreal','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Frcavliveaudio.akamaized.net%2Fhls%2Flive%2F2007000%2FMUSE%2Fadaptive_192%2Fchunklist_ao.m3u8&title=ICI+Musique+-+Montreal&key=2&location=montreal'},
                  {'name':'CBC Music','title':'Pacific','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Fcbcradiolive.akamaized.net%2Fhls%2Flive%2F2041059%2FES_R2PVC%2Fmaster.m3u8&title=CBC+Music+-+Pacific&key=2&location=vancouver'},
                  {'name':'CBC Music','title':'Eastern','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Fcbcradiolive.akamaized.net%2Fhls%2Flive%2F2041057%2FES_R2ETR%2Fmaster.m3u8&title=CBC+Music+-+Eastern&key=2&location=toronto'},
                  {'name':'CBC Music','title':'Mountain','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Fcbcradiolive.akamaized.net%2Fhls%2Flive%2F2041058%2FES_R2MED%2Fmaster.m3u8&title=CBC+Music+-+Mountain&key=2&location=edmonton'},
                  {'name':'CBC Music','title':'Central','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Fcbcradiolive.akamaized.net%2Fhls%2Flive%2F2041056%2FES_R2CWP%2Fmaster.m3u8&title=CBC+Music+-+Central&key=2&location=winnipeg'}, 
                  {'name':'CBC Music','title':'Atlantic','stream':'plugin://plugin.audio.ici-musique/?mode=stream&url=https%3A%2F%2Fcbcradiolive.akamaized.net%2Fhls%2Flive%2F2041055%2FES_R2AHF%2Fmaster.m3u8&title=CBC+Music+-+Atlantic&key=2&location=halifax'}]
PROGRAM = None
PROGRAM_SCHEDULE = None
TRACK = None
PLAYLOG = None
KEY = None
LOCATION = None
BASE_URL = sys.argv[0]
ID = BASE_URL.split('://')[1].split('/')[0]


def extract_radio_stations():
    # Initialize a set to store unique names
    unique_names = set()

    # Parse the data to extract unique names
    for item in radio_stations:
        name = item['name']
        unique_names.add(name)

    # Convert the set back to a list if needed
    unique_names = list(unique_names)
    return unique_names

def build_url(query):
    xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}: build_url: {BASE_URL} {query}")
    return BASE_URL + "?" + urlparse.urlencode(query)

def list_streams(stn):
    xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}: list_streams: {stn}")                                                                                                                                                                                                                   

    for station in radio_stations:
        if station['name'] == stn:
            url = station['stream']                                                                                                                                                                                                                                  
            station_and_title = station['name']+' '+ station['title']   
            xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}: list_streams: {station_and_title}")                                                                                                                                                                                                                   
            xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}: list_streams: {url}")
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
        xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}::update_play_item(): {tag.getTitle()}")
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
    xbmc.log(level=xbmc.LOGINFO, msg=f"{ID}: url: {url}")
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
        update_play_item()
        chill(5)
        if not PLAYER.isPlaying():
            sys.exit(0)
    

def list_stations():                                                                                                                                                                                   
    list_of_radio_stations=extract_radio_stations()
    for station in list_of_radio_stations:
        url = build_url({"mode": "folder", "foldername": station})
        xbmc.log(level=xbmc.LOGINFO, msg=f"list_station: {url}")                                                                                                                        
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