#!/usr/bin/env python

import sqlite3

def opendb():
  conn = sqlite3.connect('jukebox.db')
  conn.row_factory = sqlite3.Row
  return conn

def closedb(c):
  c.close

def get_selection_info(selection):
  conn = opendb()
  c = conn.cursor()
  c.execute('SELECT uri, metadata, type FROM jukebox_entry WHERE selection = ?', [selection])
  result=c.fetchone()
  closedb(conn)
  return result

def setupdb():
  conn = opendb()
  c = conn.cursor()
  c.execute('CREATE TABLE IF NOT EXISTS jukebox_entry (selection text, title text, artist text, uri text, metadata string, type string)')
  c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_selection ON jukebox_entry (selection)')
  c.execute('CREATE TABLE IF NOT EXISTS sonos (ip text, spotifyusername text)')
  c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_ip ON sonos (ip)')
  command = "INSERT INTO sonos (ip) SELECT '192.168.1.19' WHERE NOT EXISTS (select 1 from sonos)"
  c.execute(command)

  letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K']
  numbers = range(1, 11)
  for letter in letters:
    for number in numbers:
      selection = letter + str(number)
      command = 'INSERT OR REPLACE INTO jukebox_entry (selection, title, artist, uri, metadata, type)\
      SELECT new.selection, old.title, old.artist, old.uri, old.metadata, old.type\
      FROM (SELECT ? as selection\
      ) as new\
      LEFT JOIN (\
	  select selection, title, artist, uri, metadata, type\
	  FROM jukebox_entry\
      ) as old on old.selection = new.selection'
      c.execute(command, [selection])

  conn.commit()
  closedb(conn)

def get_sonos_info():
  conn = opendb()
  c = conn.cursor()
  c.execute('SELECT ip, spotifyusername FROM sonos')
  sonos_info = c.fetchone()
  closedb(conn)
  return sonos_info

  
def updatedb_selection(selection, artist, title, uri, metadata, type):
  conn = opendb()
  c = conn.cursor()
  c.execute('UPDATE jukebox_entry SET title = ?, artist = ?, uri = ?, metadata = ?, type = ? WHERE selection = ?', (title, artist, uri, metadata, type, selection))
  conn.commit()
  closedb(conn)
  
def updatedb_sonos(ip, spotifyusername):
  conn = opendb()
  c = conn.cursor()
  c.execute('UPDATE sonos SET ip = ?, spotifyusername = ?', (ip, spotifyusername))
  conn.commit()
  closedb(conn)
  
def get_jukebox_info():
  conn = opendb()
  c = conn.cursor()
  c.execute('SELECT selection, title, artist, uri, metadata, type FROM jukebox_entry')
  rows = c.fetchall()
  closedb(conn)
  return rows