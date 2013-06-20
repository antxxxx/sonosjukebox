#!/usr/bin/env python

import sqlite3

def opendb():
  conn = sqlite3.connect('jukebox.db')
  conn.row_factory = sqlite3.Row
  return conn

def closedb(c):
  c.close

def get_selection_info(conn, selection):
  c = conn.cursor()
  c.execute('SELECT uri, metadata, type FROM jukebox_entry WHERE selection = ?', [selection])
  result=c.fetchone()
  return result

def setupdb(conn):
  c = conn.cursor()
  c.execute('CREATE TABLE IF NOT EXISTS jukebox_entry (selection text, title text, artist text, uri text, metadata string, type string)')
  c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_selection ON jukebox_entry (selection)')
  c.execute('CREATE TABLE IF NOT EXISTS sonos (ip text)')
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

def get_sonos_info(conn):
  c = conn.cursor()
  c.execute('SELECT ip FROM sonos')
  sonos_info = c.fetchone()
  return sonos_info

  
def updatedb_selection(conn, selection, artist, title, uri, metadata, type):
  c = conn.cursor()
  c.execute('UPDATE jukebox_entry SET title = ?, artist = ?, uri = ?, metadata = ?, type = ? WHERE selection = ?', (title, artist, uri, metadata, type, selection))
  conn.commit()
  
def updatedb_sonos(conn, ip):
  c = conn.cursor()
  c.execute('UPDATE sonos SET ip = ?', (ip))
  conn.commit()
  
def get_jukebox_info(conn):
  c = conn.cursor()
  c.execute('SELECT selection, title, artist, uri, metadata, type FROM jukebox_entry')
  rows = c.fetchall()
  return rows