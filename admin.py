#!/usr/bin/env python

import cgi
import soap_templates
import db_functions
import xml.etree.ElementTree as ET
import HTMLParser
import sonos_functions

SPOTIFY_DIDL_TEMPLATE = """<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/" xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">
  <item id="00030000%s" parentID="00030000%s" restricted="true">
    <dc:title>%s</dc:title>
    <upnp:class>object.item.audioItem.musicTrack</upnp:class>
    <desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/">SA_RINCON2311_%s</desc>
  </item>
</DIDL-Lite>"""

def display_search_results(searchresults) :
  print "library search results"
  print "</p><p>"
  print "<table border=1>"
  print "<tr>"
  print "<th>artist</th>"
  print "<th>title</th>"
  print "<th>album</th>"
  print "<th>selection</th>"
  print "<th></th>"
  print "</tr>"
  
  didl=ET.fromstring(searchresults)[0][0].find('Result').text
  root=ET.fromstring(didl)
  for item in root.findall('{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}item'):
    uri=item.find('{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}res').text
    artist=item.find('{http://purl.org/dc/elements/1.1/}creator').text
    title=item.find('{http://purl.org/dc/elements/1.1/}title').text
    album=item.find('{urn:schemas-upnp-org:metadata-1-0/upnp/}album').text
    print "<tr>"
    print "<form name='addtrack' action='admin.py' method='post'>"
    print "<input type='hidden' name='action' value='add_track'>" 
    print "<input type='hidden' name='artist' value='%s'>" % artist 
    print "<input type='hidden' name='title' value='%s'>" % title
    print "<input type='hidden' name='uri' value='%s'>" % uri
    print "<input type='hidden' name='type' value='track'>" 
    print "<td>%s</td>" % repr(artist)
    print "<td>%s</td>" % repr(title)
    print "<td>%s</td>" % repr(album)
    print "<td><select name='selection'>"
    for row in jukebox_info:
	print "<option value='%s'>%s</option>" % (row["selection"], row["selection"])
    print "</select></td>"
    print "<td><input type='submit' value='assign'></td>"
    print "</form>"
    print "</tr>"
  print "</table>"

def display_spotify_search_results(spotifysearchresults) :
  sonos_info = db_functions.get_sonos_info()
  print "spotify search results"
  print "</p><p>"
  print "<table border=1>"
  print "<tr>"
  print "<th>artist</th>"
  print "<th>title</th>"
  print "<th>album</th>"
  print "<th>selection</th>"
  print "<th></th>"
  print "</tr>"
  
  searchResponse=ET.fromstring(spotifysearchresults)[0].find('{http://www.sonos.com/Services/1.1}searchResponse')
  for item in searchResponse[0].findall('{http://www.sonos.com/Services/1.1}mediaMetadata') :
    id = item.find('{http://www.sonos.com/Services/1.1}id').text
    id = id.replace(':', '%3a')
    title=item.find('{http://www.sonos.com/Services/1.1}title').text
    trackMetadata=item.find('{http://www.sonos.com/Services/1.1}trackMetadata')
    artist=trackMetadata.find('{http://www.sonos.com/Services/1.1}artist').text
    album=trackMetadata.find('{http://www.sonos.com/Services/1.1}album').text
    albumid=trackMetadata.find('{http://www.sonos.com/Services/1.1}albumId').text
    albumid = albumid.replace(':', '%3a')
    uri='x-sonos-spotify:%s?sid=9&flags=0' % id
    metadata = SPOTIFY_DIDL_TEMPLATE % (id, albumid, title, sonos_info["spotifyusername"])
    
    print "<tr>"
    print "<form name='addtrack' action='admin.py' method='post'>"
    print "<input type='hidden' name='action' value='add_track'>" 
    print "<input type='hidden' name='artist' value='%s'>" % artist 
    print "<input type='hidden' name='title' value='%s'>" % title
    print "<input type='hidden' name='uri' value='%s'>" % uri
    print "<input type='hidden' name='metadata' value='%s'>" % metadata
    print "<input type='hidden' name='type' value='track'>" 
    print "<td>%s</td>" % repr(artist)
    print "<td>%s</td>" % repr(title)
    print "<td>%s</td>" % repr(album)
    print "<td><select name='selection'>"
    for row in jukebox_info:
	print "<option value='%s'>%s</option>" % (row["selection"], row["selection"])
    print "</select></td>"
    print "<td><input type='submit' value='assign'></td>"
    print "</form>"
    print "</tr>"
  print "</table>"
  
def display_favourites() :
  print "Favourites"
  print "</p><p>"
  print "<table border=1>"
  print "<tr>"
  print "<th>artist</th>"
  print "<th>title</th>"
  print "<th>selection</th>"
  print "<th></th>"
  print "</tr>"
  favourites=sonos_functions.get_favourites()
  result=ET.fromstring(favourites)[0][0].find('Result').text
  root=ET.fromstring(result)
  for item in root.findall('{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}item') :
    uri=item.find('{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}res').text
    protocol=item.find('{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}res').attrib['protocolInfo']
    artist=item.find('{urn:schemas-rinconnetworks-com:metadata-1-0/}description').text
    title=item.find('{http://purl.org/dc/elements/1.1/}title').text
    metadata=item.find('{urn:schemas-rinconnetworks-com:metadata-1-0/}resMD').text
    print "<tr>"
    print "<form name='addtrack' action='admin.py' method='post'>"
    print "<input type='hidden' name='action' value='add_track'>" 
    print "<input type='hidden' name='artist' value='%s'>" % artist 
    print "<input type='hidden' name='title' value='%s'>" % title
    print "<input type='hidden' name='uri' value='%s'>" % uri
    print "<input type='hidden' name='metadata' value='%s'>" % metadata
    if (protocol == "x-sonosapi-stream:*:*:*") or (protocol == "x-rincon-mp3radio:*:*:*"):
      print "<input type='hidden' name='type' value='stream'>" 
    else :
      print "<input type='hidden' name='type' value='track'>" 
    print "<td>%s</td>" % artist
    print "<td>%s</td>" % title
    print "<td><select name='selection'>"
    for row in jukebox_info:
	print "<option value='%s'>%s</option>" % (row["selection"], row["selection"])
    print "</select></td>"
    print "<td><input type='submit' value='assign'></td>"
    print "</form>"
    print "</tr>"
  print "</table>"
  
def display_search_boxes() :
  print "<p>"
  print "search for a track in library"
  print "</p><p>"
  print "<form name='searchtrack' action='admin.py' method='post'>"
  print "<input type='hidden' name='action' value='search_track'>" 
  print "<input type=text name='track'>" 
  print "<input type='submit' value='Search'>"
  print "</form>"
  print "</p><p>"
  
  print "<p>"
  print "search for a track in spotify"
  print "</p><p>"
  print "<form name='searchspotify' action='admin.py' method='post'>"
  print "<input type='hidden' name='action' value='search_spotify'>" 
  print "<input type=text name='track'>" 
  print "<input type='submit' value='Search'>"
  print "</form>"
  print "</p><p>"

def display_sonos_info() :
  sonos_info = db_functions.get_sonos_info()
  print "</p><p>"
  print "sonos info"
  print "</p><p>"
  print "<table>"
  print "<form name='updatesonos' action='admin.py' method='post'>"
  print "<input type='hidden' name='action' value='update_sonos'>" 
  #print "<td><textarea name='ip' rows=1 cols=15>%s</textarea></td>" % (sonos_info["ip"])
  print "<tr>"
  print "<th>sonos ip</th>"
  print "<th>spotify username</th>"
  print "</tr>"
  print "<tr>"
  print "<td><input type=text name='ip' value='%s'></td>" % (sonos_info["ip"])
  print "<td><input type=text name='spotifyusername' value='%s'></td>" % (sonos_info["spotifyusername"])
  print "<td><input type='submit' value='Update'></td>"
  print "</tr>"
  print "</form>"
  print "</table>"
  print "</p><p>"

def display_jukebox_info():

  jukebox_info = db_functions.get_jukebox_info()
  print "jukebox selections"
  print "</p><p>"
  print "<table>"
  print "<tr>"
  print "<th>selection</th>"
  print "<th>artist</th>"
  print "<th>title</th>"
  print "<th>uri</th>"
  print "<th>metadata</th>"
  print "<th>type</th>"
  print "<th></th>"
  print "</tr>"
  for row in jukebox_info:
      print "<tr>"
      print "<form name='updatejukebox%s' action='admin.py' method='post'>" % (row["selection"])
      print "<td>%s</td>" % (row["selection"])
      print "<input type='hidden' name='selection' value=%s>" % (row["selection"])
      print "<input type='hidden' name='action' value='update_selection'>" 
      print "<td><textarea name='artist' rows=5 cols=20>%s</textarea></td>" % (row["artist"])
      print "<td><textarea name='title' rows=5 cols=20>%s</textarea></td>" % (row["title"])
      print "<td><textarea name='uri' rows=5 cols=20>%s</textarea></td>" % (row["uri"])
      print "<td><textarea name='metadata' rows=5 cols=20>%s</textarea></td>" % (row["metadata"])
      print "<td><input type='radio' name='type' value='stream' "
      if row["type"] == "stream" :
	print "checked"
      print ">stream"
      print "<input type='radio' name='type' value='track' "
      if row["type"] == "track" :
	print "checked"
      print ">track</td>"
      print "<td><input type='submit' value='Update'></td>"
      print "</form>"
      print "</tr>"
  print "</table>"
  print "</p>"



db_functions.setupdb()
searchresults = None
spotifysearchresults = None
print "Content-type: text/html"
print
form = cgi.FieldStorage() # instantiate only once!
action = form.getfirst('action', None)
if action == 'update_selection' :
  h = HTMLParser.HTMLParser()
  selection = form.getfirst('selection', None)
  artist = form.getfirst('artist', None)
  title = form.getfirst('title', None)
  uri = form.getfirst('uri', None)
  uri=h.unescape(uri)
  metadata = form.getfirst('metadata', None)
  metadata=h.unescape(metadata)
  type = form.getfirst('type', None)
  db_functions.updatedb_selection(selection, artist, title, uri, metadata, type)
elif action == 'update_sonos' :
  ip = form.getfirst('ip', None)
  spotifyusername = form.getfirst('spotifyusername', None)
  db_functions.updatedb_sonos(ip, spotifyusername)
elif action == 'search_track' :
  track = form.getfirst('track', None)
  searchresults = sonos_functions.get_search_results(track)
elif action == 'search_spotify' :
  track = form.getfirst('track', None)
  spotifysearchresults = sonos_functions.get_spotify_search_results(track)
elif action == 'add_track' :
  artist = form.getfirst('artist', None)
  title = form.getfirst('title', None)
  uri = form.getfirst('uri', None)
  metadata = form.getfirst('metadata', None)
  selection = form.getfirst('selection', None)
  type = form.getfirst('type', None)
  db_functions.updatedb_selection(selection, artist, title, uri, metadata, type)

display_search_boxes()
if (searchresults is not None) :
  display_search_results(searchresults)
if (spotifysearchresults is not None) :
  display_spotify_search_results(spotifysearchresults)
display_sonos_info()
display_favourites()
display_jukebox_info(jukebox_info)
