#!/usr/bin/python
from BeautifulSoup import BeautifulSoup
import urllib 
import sys,re
from pdb import set_trace
import time
import urllib2
import requests

URL 	= "https://www.hackthissite.org/missions/prog/12/"
LOGIN 	= "https://www.hackthissite.org/user/login"
COOKIE 	= 'PHPSESSID=kst1nvaf7td1ir16ajbkm29o72'

def get_input(input_str):
	return input_str.split('<input type="text" value=')[1].split('"')[1]

def is_prime(num):
	return num in (2,3,5,7)
	

def parse_str(string):
	sum1 = 0
	sum2 = 0
	chars = []
	for a in string:
		try:
			num = int(a)
			if num in (0,1):
				continue
			if is_prime(num):
				sum1 += num
			else:
				sum2 += num	
		except:
			chars.append(chr(ord(a)+1))
		
	prod = sum1*sum2
	return ''.join(chars[0:25])+str(prod)

def main():

	#payload = {'username': 'livne', 'password': 'rootMEin!2' , 'btn_submit': 'Login'}
	#data = urllib.urlencode(payload)
	#req = urllib2.Request(LOGIN, data)
	#opener = urllib2.build_opener()
	#opener.addheaders.append(('Referer', 'https://www.hackthissite.org/'))
	#res = opener.open(req)
	#source = res.read()
	#cookies = res.headers.getheader('set-cookie').split(';')[0]
	#print cookies

	opener = urllib2.build_opener()
	#opener.addheaders.append(('Cookie', cookies))	
	opener.addheaders.append(('Cookie', COOKIE))
	opener.addheaders.append(('Referer', 'https://www.hackthissite.org/'))
	f = opener.open(URL)
	source = f.read()
	soup = BeautifulSoup(source)
	string = get_input(str(soup.input))
				
	answer = parse_str(string)

	payload = {'solution': answer, 'submitbutton':	'1'}
	url = URL + 'index.php'
	
	data = urllib.urlencode(payload)
	req = urllib2.Request(url, data)
	opener = urllib2.build_opener()
	opener.addheaders.append(('Cookie', COOKIE))
	opener.addheaders.append(('Referer', 'https://www.hackthissite.org'))
	f = opener.open(req)
	source = f.read()
	print source
	print payload
	print string
	

if __name__ == '__main__':

	start = time.time()
	if len(sys.argv) != 1:
	    print "Usage: %s ", sys.argv[0]
	    sys.exit(1)
	main()
	print "Time: ",time.time() - start," seconds"


