#!/usr/bin/env python

import cgi
import db_functions
import sonos_functions


print "Content-type: text/html"
print
form = cgi.FieldStorage() # instantiate only once!
action = form.getfirst('action', None)
if action == 'enqueue':
  selection = form.getfirst('selection', None)
  trackinfo = db_functions.get_selection_info(selection)
  sonos_functions.enqueue_track(trackinfo)
elif action == 'play':
  sonos_functions.play_sonos()
elif action == 'pause':
  sonos_functions.pause_sonos()
