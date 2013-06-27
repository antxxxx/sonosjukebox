#!/usr/bin/env python

ENQUEUE_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Body>
<ns1:AddURIToQueue xmlns:ns1="urn:schemas-upnp-org:service:AVTransport:1">
              <InstanceID>0</InstanceID>
              <EnqueuedURI>%s</EnqueuedURI>
              <EnqueuedURIMetaData>%s</EnqueuedURIMetaData>
              <DesiredFirstTrackNumberEnqueued>0</DesiredFirstTrackNumberEnqueued>
              <EnqueueAsNext>1</EnqueueAsNext>
</ns1:AddURIToQueue>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

SET_AVTRANSPORT_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <SOAP-ENV:Body>
    <u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
      <InstanceID>0</InstanceID>
      <CurrentURI>%s</CurrentURI>
      <CurrentURIMetaData>%s</CurrentURIMetaData>
    </u:SetAVTransportURI>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

PLAY_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
  <SOAP-ENV:Body>
    <u:Play xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
      <InstanceID>0</InstanceID>
      <Speed>1</Speed>
    </u:Play>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

PAUSE_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
  <SOAP-ENV:Body>
    <u:Pause xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
      <InstanceID>0</InstanceID>
    </u:Pause>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

MEDIA_INFO_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
  <SOAP-ENV:Body>
    <u:GetMediaInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
      <InstanceID>0</InstanceID>
    </u:GetMediaInfo>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

SEEK_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <SOAP-ENV:Body>
    <u:Seek xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
      <InstanceID>0</InstanceID>
      <Unit>TRACK_NR</Unit>
      <Target>%s</Target>
    </u:Seek>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

TRANSPORT_INFO_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
  <SOAP-ENV:Body>
    <u:GetTransportInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
      <InstanceID>0</InstanceID>
    </u:GetTransportInfo>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

SEARCH_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <SOAP-ENV:Body>
    <u:Browse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">
      <ObjectID>A:TRACKS:%s</ObjectID>
      <BrowseFlag>BrowseDirectChildren</BrowseFlag>
      <Filter>dc:title,res,dc:creator,upnp:artist,upnp:album,upnp:albumArtURI</Filter>
      <StartingIndex>0</StartingIndex>
      <RequestedCount>100</RequestedCount>
      <SortCriteria></SortCriteria>
    </u:Browse>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

SPOTIFY_SEARCH_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.sonos.com/Services/1.1">
   <soapenv:Header>
     <ns:credentials>
       <ns:deviceId>%s</ns:deviceId>
       <ns:deviceProvider>Sonos</ns:deviceProvider>
       <ns:sessionId>%s</ns:sessionId>
     </ns:credentials>
   </soapenv:Header>
   <soapenv:Body>
      <ns:search>
        <ns:id>strk</ns:id>
        <ns:term>%s</ns:term>
        <ns:index>0</ns:index>
        <ns:count>10</ns:count>
      </ns:search>
   </soapenv:Body>
</soapenv:Envelope>"""

SPOTIFY_SESSION_ID = """<?xml version="1.0" encoding="utf-8"?>
<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <u:GetSessionId xmlns:u="urn:schemas-upnp-org:service:MusicServices:1">
      <ServiceId>9</ServiceId>
      <Username>%s</Username>
    </u:GetSessionId>
  </s:Body>
</s:Envelope>"""

DEVICEPROPERTIES_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
  <s:Body>
    <u:GetZoneInfo xmlns:u="urn:schemas-upnp-org:service:DeviceProperties:1" />
  </s:Body>
</s:Envelope>"""


BROWSE_FAVOURITES_TEMPLATE = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:Browse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">
      <ObjectID>FV:2</ObjectID>
      <BrowseFlag>BrowseDirectChildren</BrowseFlag>
      <Filter>dc:title,res,dc:creator,upnp:artist,upnp:album,upnp:albumArtURI</Filter>
      <StartingIndex>0</StartingIndex>
      <RequestedCount>100</RequestedCount>
      <SortCriteria></SortCriteria>
    </u:Browse>
  </s:Body>
</s:Envelope>"""