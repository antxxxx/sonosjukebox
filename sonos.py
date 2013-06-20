#!/usr/bin/env python

import cgi
import xml.etree.ElementTree as ET
import soap_templates
import db_functions
import soap_functions


def enqueue_track(sonos_info, trackinfo):
  # enqueue track
  uri = cgi.escape(trackinfo["uri"], False)
  if (trackinfo["metadata"] is not None) and (trackinfo["metadata"] != 'None') :
     metadata = cgi.escape(trackinfo["metadata"], False)
  else :
     metadata = ""
  type = trackinfo["type"]
  if type == 'track' :
    SoapMessage = soap_templates.ENQUEUE_TEMPLATE%(uri, metadata)
    EnqueueTrackResponse = soap_functions.send_soapmessage(SoapMessage, sonos_info["ip"], "/MediaRenderer/AVTransport/Control")
    # get track number
    trackno = ET.fromstring(EnqueueTrackResponse)[0][0].find('FirstTrackNumberEnqueued').text
    # get status using getmdediainfo
    statusresponse = soap_functions.send_soapmessage(soap_templates.MEDIA_INFO_TEMPLATE, sonos_info["ip"], "/MediaRenderer/AVTransport/Control")
    currenturi = ET.fromstring(statusresponse)[0][0].find('CurrentURI').text
    transportinforesponse = soap_functions.send_soapmessage(soap_templates.TRANSPORT_INFO_TEMPLATE, sonos_info["ip"], "/MediaRenderer/AVTransport/Control")
    CurrentTransportState = ET.fromstring(transportinforesponse)[0][0].find('CurrentTransportState').text
    ## if stream or not playing then start playing
    # by calling set_source with RINCON
    # set trackno
    # then call play_sonos
    if (currenturi[0:14]  != 'x-rincon-queue') or (CurrentTransportState != 'PLAYING'):
      pause_sonos()
      rincon = soap_functions.get_rincon(sonos_info["ip"])
      currenturi='x-rincon-queue:%s' % rincon
      sourcemessage = soap_templates.SET_AVTRANSPORT_TEMPLATE%(currenturi, '')
      setsourceresponse = soap_functions.send_soapmessage(sourcemessage, sonos_info["ip"], "/MediaRenderer/AVTransport/Control")
      seekmessage = soap_templates.SEEK_TEMPLATE%(trackno)
      seekmessageresponse = soap_functions.send_soapmessage(seekmessage, sonos_info["ip"], "/MediaRenderer/AVTransport/Control")
      play_sonos()
  elif type == 'stream' :
    sourcemessage = soap_templates.SET_AVTRANSPORT_TEMPLATE%(uri, metadata)
    setsourceresponse = soap_functions.send_soapmessage(sourcemessage, sonos_info["ip"], "/MediaRenderer/AVTransport/Control")
    play_sonos()

def play_sonos():
   response = soap_functions.send_soapmessage(soap_templates.PLAY_TEMPLATE, sonos_info["ip"], "/MediaRenderer/AVTransport/Control")
 
  
def pause_sonos():
   response = soap_functions.send_soapmessage(soap_templates.PAUSE_TEMPLATE, sonos_info["ip"], "/MediaRenderer/AVTransport/Control")

print "Content-type: text/html"
print
conn = db_functions.opendb()
sonos_info = db_functions.get_sonos_info(conn)
form = cgi.FieldStorage() # instantiate only once!
action = form.getfirst('action', None)
if action == 'enqueue':
  selection = form.getfirst('selection', None)
  trackinfo = db_functions.get_selection_info(conn, selection)
  enqueue_track(sonos_info, trackinfo)
elif action == 'play':
  play_sonos()
elif action == 'pause':
  pause_sonos()
db_functions.closedb(conn)