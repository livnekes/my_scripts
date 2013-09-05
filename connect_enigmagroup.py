#!/usr/bin/python
from BeautifulSoup import BeautifulSoup
import urllib 
import sys,re
from pdb import set_trace
import time
import urllib2
import requests
import cookielib
from requests import session

REFERER  = 	"http://www.enigmagroup.org/forums/index.php"
SITE 	 = 	"http://www.enigmagroup.org/"
LOGIN 	 = 	"http://www.enigmagroup.org/forums/login2/"
USERNAME = 	None	
PASSWORD = 	None

def send_http_post(cookies, url, payload = {}):
	""" Send data via http post command """

	data = urllib.urlencode(payload)
	req = urllib2.Request(url, data)
	opener = urllib2.build_opener()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
	opener.addheaders.append(('Referer', REFERER))

	try:
		f = opener.open(req)
		source = f.read()
		print source
	except:
		print 'failed to send'

def get_url_cookies():
	""" Login to url and retrive cookies """

	payload = {
	    'user'		: USERNAME,
	    'passwrd'		: PASSWORD,
	    'cookielength'	: '-1',
	}

	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders.append(('Referer', REFERER))
	login_data = urllib.urlencode(payload)
	resp = opener.open(LOGIN, login_data)
	resp.close()

	return cj

def main():
	global USERNAME, PASSWORD

	USERNAME = sys.argv[1]
	PASSWORD = sys.argv[2]
	print USERNAME,PASSWORD

	url = 'http://www.enigmagroup.org/missions/basics/um/2/%2527/'
	cookies = get_url_cookies()
	send_http_post(cookies,url)

if __name__ == '__main__':

	start = time.time()
	if len(sys.argv) != 3:
	    print "Usage: %s Username Password", sys.argv[0]
	    sys.exit(1)
	main()
	print "Time: ",time.time() - start," seconds"


