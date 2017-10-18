#!/usr/bin/python3

import urllib.request, json
import urllib.parse as urlparse

GOOGLE_API_KEY='AIzaSyCC8ijUZfPSVU64U1qFOHuzfHxKyuYAT8M'
GOOGLE_GEOCODING_QUERY='https://maps.googleapis.com/maps/api/geocode/json?address={}&key='+GOOGLE_API_KEY

def geoLookupGoogle(address):
	query=GOOGLE_GEOCODING_QUERY.format(urlparse.quote(address));
	print(query)
	with urllib.request.urlopen(query,None,3) as url:
		data = json.loads(url.read().decode())
		print(data)
		

	
if __name__=='__main__':
	geoLookupGoogle('stinchcomb dr. and olentangy')
	