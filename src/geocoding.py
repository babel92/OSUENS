#!/usr/bin/python3

import urllib.request, json
import urllib.parse as urlparse
import KEY
import time
import code

GOOGLE_GEOCODING_QUERY='https://maps.googleapis.com/maps/api/geocode/json?address={}&key='+KEY.GOOGLE_API_KEY

def geoLookupGoogle(address):
	# Add some guard words to restrict search results, we don't even need to
	# perform any duplication check since the Google API will handle this nicely
	address += ',columbus,oh'
	query=GOOGLE_GEOCODING_QUERY.format(urlparse.quote(address));

	try:
		with urllib.request.urlopen(query,None,3) as url:
			data = json.loads(url.read().decode())
			return data
	except:
		print('Failed to contact Google Geocoding API')
		return {'status':'Network problem'}

def extractGeoInfo(dict):
	if dict['status'] !='OK':
		print('GeoInfo error')
	coord=dict['results'][0]['geometry']['location']
	return {'coord':[coord['lat'],coord['lng']]}

def addrsToInfoList(al):
	if isinstance(al,str):
		al=al.split('\n')
	return [extractGeoInfo(geoLookupGoogle(e)) for e in al]

if __name__=='__main__':
	a=addrsToInfoList('516 stinchcomb dr.')
	code.interact(local=locals())
