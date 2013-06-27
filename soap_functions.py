#!/usr/bin/env python
import xml.etree.ElementTree as ET
import httplib
import socket
import zlib

def send_soapmessage(SoapMessage, host, service, protocol, soapaction):
  if protocol == "https" :
    webservice = httplib.HTTPSConnection(host)
  else :
    webservice = httplib.HTTPConnection(host)
  webservice.putrequest("POST", service)
  myip=socket.gethostbyname(socket.gethostname())
  webservice.putheader("Host", myip)
  webservice.putheader("User-Agent", "Python post")
  webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
  webservice.putheader("Content-length", "%d" % len(SoapMessage))
  #root = ET.fromstring(SoapMessage)
  #soapaction=root[1][0].tag
  #soapaction=soapaction.replace('{', '').replace('}', '#')
  webservice.putheader("SOAPAction", soapaction)
  webservice.endheaders()
  webservice.send(SoapMessage)
  response = webservice.getresponse()
  if (response.getheader('Content-Encoding') == 'gzip') :
    SoapResponse = zlib.decompress(response.read(), 16+zlib.MAX_WBITS)
  else :
    SoapResponse = response.read()
  return SoapResponse

def get_rincon(sonos_ip) :
  htcon="%s:1400"%(sonos_ip)
  conn = httplib.HTTPConnection(htcon)
  conn.request("GET", "/xml/device_description.xml")
  r1 = conn.getresponse()
  data1 = r1.read()
  root=ET.fromstring(data1)
  device=root.find('{urn:schemas-upnp-org:device-1-0}device')
  rincon=device.find('{urn:schemas-upnp-org:device-1-0}UDN').text
  rincon=rincon.replace('uuid:', '') + '#0'
  return rincon

def get_sonos_endpoint(sonos_ip) :
  sonos_endpoint = "%s:1400" %(sonos_ip)
  return sonos_endpoint