#!/usr/bin/env python
import cgi
import soap_templates
import db_functions
import xml.etree.ElementTree as ET
import HTMLParser
import sonos_functions
import urllib

printstripsurl = "http://ripley/simplestripper/printstrips.php"
optionstemplate = """<table border="1" cellspacing="0" cellpadding="3">
    <tbody>
      <tr>
        <td>Color</td>
        <td>Background</td>
        <td>Font</td>
        <td>Print Size</td>
      </tr>
      <tr>
        <td>
          <input type="radio" name="color" value="red" checked="checked">
          <span style="color: rgb(255, 0, 0);">Red</span><br>
          <input type="radio" name="color" value="blue">
          <span style="color: rgb(0, 0, 255);">Blue</span><br>
          <input type="radio" name="color" value="purple">
          <span style="color: rgb(128, 0, 128);">Purple</span><br>
          <input type="radio" name="color" value="green">
          <span style="color: rgb(0, 128, 0);">Green</span><br>
        </td>
        <td>
          <input type="radio" name="background" value="TRUE">Yes<br>
          <input type="radio" name="background" value="" checked="checked">No<br>
        </td>
        <td>
          <input type="radio" name="titlefont" value="Times">Times<br>
          <input type="radio" name="titlefont" value="Helvetica">Helvetica<br>
          <input type="radio" name="titlefont" value="Courier" checked="checked">Courier<br>
        </td>
        <td> 
          <input type="radio" name="titlesize" value="small">Small<br>
          <input type="radio" name="titlesize" value="medium" checked="checked">Medium<br>
          <input type="radio" name="titlesize" value="large">Large<br>
        </td>
      </tr>
    </tbody>
  </table>
"""

def display_jukebox_info():

  jukebox_info = db_functions.get_jukebox_info()
  print "jukebox selections"
  print "</p><p>"
  print "<table>"
  print "<tr>"
  print "<th>selection</th>"
  print "<th>artist</th>"
  print "<th>title</th>"
  print "</tr>"
  for row in jukebox_info:
      print "<tr>"
      print "<td>%s</td>" % (row["selection"])
      print "<td>%s</td>" % (row["artist"])
      print "<td>%s</td>" % (row["title"])
      print "</tr>"
  print "</table>"
  print "</p>"

def print_strips():
  jukebox_info = db_functions.get_jukebox_info()
  print "print title strip"
  print "</p><p>"
  print "There are 40 tracks printed per page - PDF 1 is tracks A1 to D10, PDF 2 is track E1 to H10 and PDF 3 is track I10 to K10"
  print "</p><p>"
  print '<form method="post" action="%s" name="record_entry">' % (printstripsurl)
  print optionstemplate

  i = 1
  j = 0
  for row in jukebox_info:
    selection_number=row["selection"][1:]
    if ((int(selection_number) % 2) == 1) :
      print "<input type='hidden' name='artista[%s]' value='%s'>" % ((i//2) + 1, (urllib.quote(row["artist"] or '')))
      print "<input type='hidden' name='titlea[%s]' value='%s'>" % ((i//2) + 1, (urllib.quote(row["title"] or '')))
    else :
      print "<input type='hidden' name='artistb[%s]' value='%s'>" % (i/2, (urllib.quote(row["artist"] or '')))
      print "<input type='hidden' name='titleb[%s]' value='%s'>" % (i/2, (urllib.quote(row["title"] or '')))
    i = i + 1
    if (i > 40) :
      i = 1
      j = j + 1
      print "</p>"
      print "<button name='Submit' type='submit'>Create PDF %s </button><br>""" % (j)
      print "</form>"
      print '<form method="post" action="%s" name="record_entry">' % (printstripsurl)
      print optionstemplate

  print "</p>"
  print "<button name='Submit' type='submit'>Create PDF %s </button><br>" % (j+1)
  print "</form>"
  print "</p>"
  
print "Content-type: text/html"
print
print_strips()
display_jukebox_info()
