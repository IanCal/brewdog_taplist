from bs4 import BeautifulSoup
from requests import get
from cachetools import TTLCache, cached
from bottle import route, run
import os


cache = TTLCache(1000, 600)

@cached(cache=cache)
def get_taplist(location, bar):
	url = "https://www.brewdog.com/bars/%s/%s" % (location,bar)
	page = BeautifulSoup(get(url).text, 'html.parser')
	beers = page.find_all('ul', class_='beer')
	taplist = []
	for beer in beers:
	    entries = beer.find_all('span')
	    taplist.append({
	        'name': entries[0].string,
	        'style': entries[1].string,
	        'size': entries[2].string,
	        'brewery': entries[3].string,
	        'strength': entries[4].string
	    })
	return taplist

@route('/<location>/<bar>')
def taplist_endpoint(location, bar):
	taplist = get_taplist(location, bar)
	return {"taplist": taplist}

run(host='0.0.0.0', port=int(os.getenv('PORT', '8080')))