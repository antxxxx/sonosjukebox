#!/usr/bin/env python

import cgi
import soap_templates
import db_functions
import soap_functions
import xml.etree.ElementTree as ET
import HTMLParser

def display_page(sonos_info, jukebox_info, searchresults):
  
  print "<p>"
  print "search for a track"
  print "</p><p>"
  print "<form name='searchtrack' action='admin.py' method='post'>"
  print "<input type='hidden' name='action' value='search_track'>" 
  print "<input type=text name='track'>" 
  print "<input type='submit' value='Search'>"
  print "</form>"
  print "</p><p>"
  
  if (searchresults is not None) :
    print "search results"
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
      print "<td>%s</td>" % artist
      print "<td>%s</td>" % title
      print "<td>%s</td>" % album
      print "<td><select name='selection'>"
      for row in jukebox_info:
         print "<option value='%s'>%s</option>" % (row["selection"], row["selection"])
      print "</select></td>"
      print "<td><input type='submit' value='assign'></td>"
      print "</form>"
      print "</tr>"
    print "</table>"
    
  print "</p><p>"
  print "sonos ip address"
  print "</p><p>"
  print "<form name='updatesonos' action='admin.py' method='post'>"
  print "<input type='hidden' name='action' value='update_sonos'>" 
  #print "<td><textarea name='ip' rows=1 cols=15>%s</textarea></td>" % (sonos_info["ip"])
  print "<input type=text name='ip' value='%s'>" % (sonos_info["ip"])
  print "<input type='submit' value='Update'>"
  print "</form>"
  print "</p><p>"

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


def get_search_results(track, sonos_info) :
  SoapMessage = soap_templates.SEARCH_TEMPLATE%(track)
  SearchResponse = soap_functions.send_soapmessage(SoapMessage, sonos_info["ip"], "/MediaServer/ContentDirectory/Control")
  return SearchResponse

conn = db_functions.opendb()
db_functions.setupdb(conn)
searchresults = None
sonos_info = db_functions.get_sonos_info(conn)
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
  db_functions.updatedb_selection(conn, selection, artist, title, uri, metadata, type)
elif action == 'update_sonos' :
  ip = form.getfirst('ip', None)
  db_functions.updatedb_sonos(conn, ip)
elif action == 'search_track' :
  track = form.getfirst('track', None)
  searchresults = get_search_results(track, sonos_info)
elif action == 'add_track' :
  artist = form.getfirst('artist', None)
  title = form.getfirst('title', None)
  uri = form.getfirst('uri', None)
  selection = form.getfirst('selection', None)
  db_functions.updatedb_selection(conn, selection, artist, title, uri, None, 'track')
  
  


jukebox_info = db_functions.get_jukebox_info(conn)
display_page(sonos_info, jukebox_info, searchresults)
db_functions.closedb(conn)