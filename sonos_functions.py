#!/usr/bin/env python

import xml.etree.ElementTree as ET
import soap_templates
import db_functions
import soap_functions
import db_functions
import cgi


def enqueue_track(trackinfo):
  sonos_info = db_functions.get_sonos_info()
  # enqueue track
  uri = cgi.escape(trackinfo["uri"], False)
  if (trackinfo["metadata"] is not None) and (trackinfo["metadata"] != 'None') :
     metadata = cgi.escape(trackinfo["metadata"], False)
  else :
     metadata = ""
  type = trackinfo["type"]
  if type == 'track' :
    SoapMessage = soap_templates.ENQUEUE_TEMPLATE%(uri, metadata)
    EnqueueTrackResponse = soap_functions.send_soapmessage(SoapMessage, 
							   soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
							   "/MediaRenderer/AVTransport/Control",
							   "http",
							   "urn:schemas-upnp-org:service:AVTransport:1#AddURIToQueue")
    # get track number
    trackno = ET.fromstring(EnqueueTrackResponse)[0][0].find('FirstTrackNumberEnqueued').text
    # get status using getmdediainfo
    statusresponse = soap_functions.send_soapmessage(soap_templates.MEDIA_INFO_TEMPLATE, 
						     soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
						     "/MediaRenderer/AVTransport/Control",
						     "http",
						     "urn:schemas-upnp-org:service:AVTransport:1#GetMediaInfo")
    currenturi = ET.fromstring(statusresponse)[0][0].find('CurrentURI').text
    transportinforesponse = soap_functions.send_soapmessage(soap_templates.TRANSPORT_INFO_TEMPLATE, 
							    soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
							    "/MediaRenderer/AVTransport/Control",
							    "http",
							    "urn:schemas-upnp-org:service:AVTransport:1#GetTransportInfo")
    CurrentTransportState = ET.fromstring(transportinforesponse)[0][0].find('CurrentTransportState').text
    ## if stream or not playing then start playing
    # by calling set_source with RINCON
    # set trackno
    # then call play_sonos
    start_playing = 0
    if currenturi == None :
      start_playing = 1
    else :
      if (currenturi[0:14]  != 'x-rincon-queue') or (CurrentTransportState != 'PLAYING') :
	start_playing = 1
    if start_playing == 1 :
      pause_sonos()
      rincon = soap_functions.get_rincon(sonos_info["ip"])
      currenturi='x-rincon-queue:%s' % rincon
      sourcemessage = soap_templates.SET_AVTRANSPORT_TEMPLATE%(currenturi, '')
      setsourceresponse = soap_functions.send_soapmessage(sourcemessage, 
							  soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
							  "/MediaRenderer/AVTransport/Control",
							  "http",
							  "urn:schemas-upnp-org:service:AVTransport:1#SetAVTransportURI")
      seekmessage = soap_templates.SEEK_TEMPLATE%(trackno)
      seekmessageresponse = soap_functions.send_soapmessage(seekmessage, 
							    soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
							    "/MediaRenderer/AVTransport/Control",
							    "http",
							    "urn:schemas-upnp-org:service:AVTransport:1#Seek")
      play_sonos()
  elif type == 'stream' :
    sourcemessage = soap_templates.SET_AVTRANSPORT_TEMPLATE%(uri, metadata)
    setsourceresponse = soap_functions.send_soapmessage(sourcemessage, 
							soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
							"/MediaRenderer/AVTransport/Control",
							"http",
							"urn:schemas-upnp-org:service:AVTransport:1#SetAVTransportURI")
    print sourcemessage
    print setsourceresponse
    play_sonos()

def play_sonos():
  sonos_info = db_functions.get_sonos_info()
  response = soap_functions.send_soapmessage(soap_templates.PLAY_TEMPLATE, 
					      soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
					      "/MediaRenderer/AVTransport/Control",
					      "http",
					      "urn:schemas-upnp-org:service:AVTransport:1#Play")
 
  
def pause_sonos():
  sonos_info = db_functions.get_sonos_info()
  response = soap_functions.send_soapmessage(soap_templates.PAUSE_TEMPLATE, 
					      soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
					      "/MediaRenderer/AVTransport/Control",
					      "http",
					      "urn:schemas-upnp-org:service:AVTransport:1#Pause")

def get_search_results(track) :
  sonos_info = db_functions.get_sonos_info()
  SoapMessage = soap_templates.SEARCH_TEMPLATE%(track)
  SearchResponse = soap_functions.send_soapmessage(SoapMessage, 
						   soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
						   "/MediaServer/ContentDirectory/Control", 
						   "http", 
						   "urn:schemas-upnp-org:service:ContentDirectory:1#Browse")
  return SearchResponse

def get_spotify_session_id() :
  sonos_info = db_functions.get_sonos_info()
  SoapMessage = soap_templates.SPOTIFY_SESSION_ID%(sonos_info["spotifyusername"])
  sessionidrespones= soap_functions.send_soapmessage(SoapMessage, 
						     soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
						     "/MusicServices/Control", 
						     "http", 
						     "urn:schemas-upnp-org:service:MusicServices:1#GetSessionId")
  sessionid = ET.fromstring(sessionidrespones)[0][0].find('SessionId').text
  return sessionid

def get_spotify_search_results(track) :
  SoapMessage = soap_templates.SPOTIFY_SEARCH_TEMPLATE%(get_serial_number(), get_spotify_session_id(), track)
  SearchResponse = soap_functions.send_soapmessage(SoapMessage, 
						   "spotify.ws.sonos.com", 
						   "/smapi", 
						   "https", 
						   '"http://www.sonos.com/Services/1.1#search"')
  SearchResponse=SearchResponse.replace('\n', '')
  SearchResponse=SearchResponse.replace('\t', '')
  return SearchResponse

def get_serial_number() :
  sonos_info = db_functions.get_sonos_info()
  response = soap_functions.send_soapmessage(soap_templates.DEVICEPROPERTIES_TEMPLATE, 
					      soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
					      "/DeviceProperties/Control",
					      "http",
					      "urn:schemas-upnp-org:service:DeviceProperties:1#GetZoneInfo")
  serial_number = ET.fromstring(response)[0][0].find('SerialNumber').text
  return serial_number

def get_favourites() :
  sonos_info = db_functions.get_sonos_info()
  response = soap_functions.send_soapmessage(soap_templates.BROWSE_FAVOURITES_TEMPLATE, 
					      soap_functions.get_sonos_endpoint(sonos_info["ip"]), 
					      "/MediaServer/ContentDirectory/Control",
					      "http",
					      "urn:schemas-upnp-org:service:ContentDirectory:1#Browse")
  return response
# http://192.168.1.19:1400/status/securesettings to get username for spotify
